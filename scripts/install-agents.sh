#!/bin/sh
# Install Orchestra's exact custom-agent profiles without editing Codex config.

set -eu

usage() {
  cat <<'EOF'
Usage: install-agents.sh [--target-dir PATH] [--check] [--check-role ROLE ...] [--update]

Install Orchestra's Luna, Terra, and Sol profiles. Existing differing files are
never overwritten by default. --check is read-only; --check-role accepts luna, terra,
or sol. --update replaces only recognized Orchestra profiles and keeps backups.
EOF
}

fail() {
  printf '%s\n' "ERROR: $*" >&2
  exit 1
}

path_exists() {
  [ -e "$1" ] || [ -L "$1" ]
}

state_of() {
  destination=$1
  template=$2
  if ! path_exists "$destination"; then
    printf '%s\n' missing
  elif [ -L "$destination" ] || [ ! -f "$destination" ]; then
    printf '%s\n' unsafe
  elif cmp -s "$template" "$destination"; then
    printf '%s\n' current
  else
    printf '%s\n' conflict
  fi
}

role_selected() {
  role=$1
  [ -z "$check_roles" ] && return 0
  case ",$check_roles," in
    *,"$role",*) return 0 ;;
    *) return 1 ;;
  esac
}

has_exact_line_once() {
  candidate_path=$1
  expected_line=$2
  [ "$(grep -Fxc "$expected_line" "$candidate_path" || true)" -eq 1 ]
}

profile_is_recognized() {
  candidate_path=$1
  candidate_role=$2
  case "$candidate_role" in
    luna)
      has_exact_line_once "$candidate_path" 'name = "orchestra_luna_implementer"' &&
        has_exact_line_once "$candidate_path" 'model = "gpt-5.6-luna"' &&
        has_exact_line_once "$candidate_path" 'model_reasoning_effort = "max"'
      ;;
    terra)
      has_exact_line_once "$candidate_path" 'name = "orchestra_terra_implementer"' &&
        has_exact_line_once "$candidate_path" 'model = "gpt-5.6-terra"' &&
        has_exact_line_once "$candidate_path" 'model_reasoning_effort = "high"'
      ;;
    sol)
      has_exact_line_once "$candidate_path" 'name = "orchestra_sol_reviewer"' &&
        has_exact_line_once "$candidate_path" 'model = "gpt-5.6-sol"' &&
        has_exact_line_once "$candidate_path" 'model_reasoning_effort = "high"' &&
        has_exact_line_once "$candidate_path" 'sandbox_mode = "read-only"'
      ;;
    *) return 1 ;;
  esac && has_exact_line_once "$candidate_path" 'developer_instructions = """'
}

install_missing() {
  template=$1
  destination=$2
  staged=$(mktemp "$target_dir/.orchestra-agent.XXXXXX") ||
    fail "could not stage profile: $destination"
  if ! cp "$template" "$staged"; then
    rm -f "$staged"
    fail "could not stage profile: $destination"
  fi
  if ! ln "$staged" "$destination"; then
    rm -f "$staged"
    fail "destination appeared during install and was not overwritten: $destination"
  fi
  rm -f "$staged" || fail "could not remove staged profile: $staged"
  printf '%s\n' "INSTALLED: $destination"
}

update_recognized() {
  template=$1
  destination=$2
  role=$3
  expected_fingerprint=$4

  [ "$(cksum "$destination")" = "$expected_fingerprint" ] ||
    fail "destination changed after update preflight: $destination"
  profile_is_recognized "$destination" "$role" ||
    fail "destination is no longer a recognized Orchestra $role profile"

  backup=$(mktemp "$target_dir/.orchestra-$role-backup.XXXXXX") ||
    fail "could not create backup for: $destination"
  if ! cp "$destination" "$backup"; then
    rm -f "$backup"
    fail "could not back up profile: $destination"
  fi

  staged=$(mktemp "$target_dir/.orchestra-agent.XXXXXX") || {
    rm -f "$backup"
    fail "could not stage profile: $destination"
  }
  if ! cp "$template" "$staged"; then
    rm -f "$staged" "$backup"
    fail "could not stage profile: $destination"
  fi
  if ! mv -f "$staged" "$destination"; then
    rm -f "$staged"
    fail "could not atomically update profile; backup kept at: $backup"
  fi
  printf '%s\n' "UPDATED: $destination"
  printf '%s\n' "BACKUP: $backup"
}

script_dir=$(CDPATH= cd "$(dirname "$0")" && pwd) || exit 1
template_dir=$script_dir/../agents

if [ -n "${CODEX_HOME-}" ]; then
  target_dir=$CODEX_HOME/agents
else
  [ -n "${HOME-}" ] || fail "HOME is unset; pass --target-dir."
  target_dir=$HOME/.codex/agents
fi

check_only=0
check_roles=''
update_existing=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --target-dir)
      [ "$#" -ge 2 ] && [ -n "$2" ] || fail "--target-dir requires a path."
      case "$2" in --*) fail "--target-dir must be an explicit path." ;; esac
      target_dir=$2
      shift 2
      ;;
    --check)
      check_only=1
      shift
      ;;
    --check-role)
      [ "$#" -ge 2 ] || fail "--check-role requires luna, terra, or sol."
      case "$2" in luna|terra|sol) ;; *) fail "unknown role: $2" ;; esac
      check_only=1
      check_roles=$check_roles$2,
      shift 2
      ;;
    --update)
      update_existing=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

[ "$check_only" -eq 0 ] || [ "$update_existing" -eq 0 ] ||
  fail "--update cannot be combined with --check or --check-role."

case "$target_dir" in
  /*) ;;
  *) target_dir=$(pwd -P)/$target_dir ;;
esac
case "$target_dir" in /|//) fail "refusing filesystem root target" ;; esac

luna_template=$template_dir/orchestra-luna-implementer.toml
terra_template=$template_dir/orchestra-terra-implementer.toml
sol_template=$template_dir/orchestra-sol-reviewer.toml
luna_destination=$target_dir/orchestra-luna-implementer.toml
terra_destination=$target_dir/orchestra-terra-implementer.toml
sol_destination=$target_dir/orchestra-sol-reviewer.toml

for template in "$luna_template" "$terra_template" "$sol_template"; do
  [ -f "$template" ] && [ ! -L "$template" ] ||
    fail "missing or unsafe shipped profile: $template"
done

if path_exists "$target_dir"; then
  [ -d "$target_dir" ] && [ ! -L "$target_dir" ] ||
    fail "target is not a real directory: $target_dir"
fi

luna_state=$(state_of "$luna_destination" "$luna_template")
terra_state=$(state_of "$terra_destination" "$terra_template")
sol_state=$(state_of "$sol_destination" "$sol_template")

luna_fingerprint=''
terra_fingerprint=''
sol_fingerprint=''
if [ "$update_existing" -eq 1 ]; then
  if [ "$luna_state" = conflict ]; then
    profile_is_recognized "$luna_destination" luna || fail "Luna conflict is not a recognized Orchestra profile; no files changed"
    luna_fingerprint=$(cksum "$luna_destination")
  fi
  if [ "$terra_state" = conflict ]; then
    profile_is_recognized "$terra_destination" terra || fail "Terra conflict is not a recognized Orchestra profile; no files changed"
    terra_fingerprint=$(cksum "$terra_destination")
  fi
  if [ "$sol_state" = conflict ]; then
    profile_is_recognized "$sol_destination" sol || fail "Sol conflict is not a recognized Orchestra profile; no files changed"
    sol_fingerprint=$(cksum "$sol_destination")
  fi
fi

if [ "$check_only" -eq 1 ]; then
  if role_selected luna; then [ "$luna_state" = current ] || fail "Luna profile is $luna_state"; fi
  if role_selected terra; then [ "$terra_state" = current ] || fail "Terra profile is $terra_state"; fi
  if role_selected sol; then [ "$sol_state" = current ] || fail "Sol profile is $sol_state"; fi
  printf '%s\n' "CHECK PASSED: selected Orchestra profiles exactly match."
  exit 0
fi

for state in "$luna_state" "$terra_state" "$sol_state"; do
  case "$state" in
    current|missing) ;;
    conflict) [ "$update_existing" -eq 1 ] || fail "conflicting destination; use --update only for recognized Orchestra profiles" ;;
    *) fail "conflicting or unsafe destination; no files changed" ;;
  esac
done

if [ ! -d "$target_dir" ]; then
  mkdir -p "$target_dir" || fail "could not create target directory"
fi
[ -d "$target_dir" ] && [ ! -L "$target_dir" ] || fail "target changed after preflight"

[ "$(state_of "$luna_destination" "$luna_template")" = "$luna_state" ] || fail "Luna destination changed after preflight"
[ "$(state_of "$terra_destination" "$terra_template")" = "$terra_state" ] || fail "Terra destination changed after preflight"
[ "$(state_of "$sol_destination" "$sol_template")" = "$sol_state" ] || fail "Sol destination changed after preflight"

case "$luna_state" in
  current) ;;
  missing) install_missing "$luna_template" "$luna_destination" ;;
  conflict) update_recognized "$luna_template" "$luna_destination" luna "$luna_fingerprint" ;;
esac
case "$terra_state" in
  current) ;;
  missing) install_missing "$terra_template" "$terra_destination" ;;
  conflict) update_recognized "$terra_template" "$terra_destination" terra "$terra_fingerprint" ;;
esac
case "$sol_state" in
  current) ;;
  missing) install_missing "$sol_template" "$sol_destination" ;;
  conflict) update_recognized "$sol_template" "$sol_destination" sol "$sol_fingerprint" ;;
esac

cmp -s "$luna_template" "$luna_destination" || fail "Luna post-install check failed"
cmp -s "$terra_template" "$terra_destination" || fail "Terra post-install check failed"
cmp -s "$sol_template" "$sol_destination" || fail "Sol post-install check failed"
printf '%s\n' "INSTALL PASSED: Luna, Terra, and Sol profiles exactly match."
