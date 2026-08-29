#!/bin/sh
# Install Orchestra's exact custom-agent profiles without editing Codex config.

set -eu

usage() {
  cat <<'EOF'
Usage: install-agents.sh [--target-dir PATH] [--check] [--check-role ROLE ...]

Install Orchestra's Luna, Terra, and Sol profiles. Existing differing files are
never overwritten. --check is read-only; --check-role accepts luna, terra, or sol.
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
    --help|-h)
      usage
      exit 0
      ;;
    *)
      fail "unknown argument: $1"
      ;;
  esac
done

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

if [ "$check_only" -eq 1 ]; then
  if role_selected luna; then [ "$luna_state" = current ] || fail "Luna profile is $luna_state"; fi
  if role_selected terra; then [ "$terra_state" = current ] || fail "Terra profile is $terra_state"; fi
  if role_selected sol; then [ "$sol_state" = current ] || fail "Sol profile is $sol_state"; fi
  printf '%s\n' "CHECK PASSED: selected Orchestra profiles exactly match."
  exit 0
fi

for state in "$luna_state" "$terra_state" "$sol_state"; do
  case "$state" in current|missing) ;; *) fail "conflicting or unsafe destination; no files changed" ;; esac
done

if [ ! -d "$target_dir" ]; then
  mkdir -p "$target_dir" || fail "could not create target directory"
fi
[ -d "$target_dir" ] && [ ! -L "$target_dir" ] || fail "target changed after preflight"

[ "$(state_of "$luna_destination" "$luna_template")" = "$luna_state" ] || fail "Luna destination changed after preflight"
[ "$(state_of "$terra_destination" "$terra_template")" = "$terra_state" ] || fail "Terra destination changed after preflight"
[ "$(state_of "$sol_destination" "$sol_template")" = "$sol_state" ] || fail "Sol destination changed after preflight"

[ "$luna_state" = current ] || install_missing "$luna_template" "$luna_destination"
[ "$terra_state" = current ] || install_missing "$terra_template" "$terra_destination"
[ "$sol_state" = current ] || install_missing "$sol_template" "$sol_destination"

cmp -s "$luna_template" "$luna_destination" || fail "Luna post-install check failed"
cmp -s "$terra_template" "$terra_destination" || fail "Terra post-install check failed"
cmp -s "$sol_template" "$sol_destination" || fail "Sol post-install check failed"
printf '%s\n' "INSTALL PASSED: Luna, Terra, and Sol profiles exactly match."
