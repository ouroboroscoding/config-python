# config_oc releases

## 1.1.1
- Fixed a bug where if a requested config value was a non-dict but the default
was a dict, a merge was attempted that would always fail.
- Added `config.on_reload()` to allow scripts to register a callback if the
config is ever reloaded.

# 1.1.0
- Added `config.reload()` to force `config` to re-fetch config files from the
disk.