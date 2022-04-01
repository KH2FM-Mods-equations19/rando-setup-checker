import json
import os
from pathlib import Path
from typing import Optional

import yaml


class ConfigurationCheckResult:

    def __init__(self, name: str):
        self.name = name
        self.infos: [str] = []
        self.errors: [str] = []


class PcRandoConfiguration:

    def __init__(
            self,
            game_install_path: Optional[Path] = None,
            openkh_path: Optional[Path] = None,
            games_extract_path: Optional[Path] = None,
            mods_manager_bridge_path: Optional[Path] = None,
            patches_path: Optional[Path] = None
    ):
        self.game_install_path = game_install_path
        self.openkh_path = openkh_path
        self.games_extract_path = games_extract_path
        self.mods_manager_bridge_path = mods_manager_bridge_path
        self.patches_path = patches_path

    @staticmethod
    def read_from_mods_manager_bridge(mods_manager_bridge_path: Optional[Path]):
        if not mods_manager_bridge_path:
            return PcRandoConfiguration(mods_manager_bridge_path=mods_manager_bridge_path)

        if not mods_manager_bridge_path.is_dir():
            return PcRandoConfiguration(mods_manager_bridge_path=mods_manager_bridge_path)

        config_file = mods_manager_bridge_path / 'config.json'
        if not config_file.is_file():
            return PcRandoConfiguration(mods_manager_bridge_path=mods_manager_bridge_path)

        with open(config_file) as file:
            raw = json.load(file)
            return PcRandoConfiguration(
                game_install_path=path_or_none(raw.get('khgame_path', '')),
                openkh_path=path_or_none(raw.get('openkh_path', '')),
                games_extract_path=path_or_none(raw.get('extracted_games_path', '')),
                mods_manager_bridge_path=mods_manager_bridge_path,
                patches_path=path_or_none(raw.get('patches_path', ''))
            )

    def validate_all(self) -> [ConfigurationCheckResult]:
        return [
            self._validate_mods_manager_bridge(),
            self._validate_game_install(),
            self._validate_openkh(),
            self._validate_games_extract(),
            self._validate_patches(),
            self._validate_lua_scripts()
        ]

    def _validate_mods_manager_bridge(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Mods Manager Bridge location')

        bridge_path = self.mods_manager_bridge_path
        if not bridge_path:
            result.errors.append('Mods Manager Bridge location not chosen')
            return result

        if not bridge_path.is_dir():
            result.errors.append('Mods Manager Bridge location does not exist')
            return result

        result.infos.append('Found Mods Manager Bridge location [{}]'.format(bridge_path))

        exe_path = bridge_path / 'build_from_mm.exe'
        if not exe_path.is_file():
            result.errors.append('Mods Manager Bridge location does not contain `build_from_mm.exe`')
            return result

        result.infos.append('Found Mods Manager Bridge executable')

        configuration_file = bridge_path / 'config.json'
        if not configuration_file.is_file():
            result.errors.append('Mods Manager Bridge has not been configured yet')
            return result

        result.infos.append('Found Mods Manager Bridge configuration file')

        return result

    def _validate_game_install(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Game Install location')

        game_path = self.game_install_path
        if not game_path:
            result.errors.append('Game Install location not configured in Mods Manager Bridge')
            return result

        if not game_path.is_dir():
            result.errors.append('Game Install location [{}] does not exist'.format(game_path))
            return result

        result.infos.append('Found Game Install location [{}]'.format(game_path))

        kh2_exe_path = game_path / 'KINGDOM HEARTS II FINAL MIX.exe'
        if not kh2_exe_path.is_file():
            result.errors.append('Game Install location is missing `KINGDOM HEARTS II FINAL MIX.exe`')
            return result

        result.infos.append('Found KH2 game executable')

        luabackend_dll_path = game_path / 'DBGHELP.dll'
        if not luabackend_dll_path.is_file():
            result.errors.append('Game Install location is missing the `DBGHELP.dll` file for LuaBackend Hook')
            return result

        result.infos.append('Found LuaBackend Hook DLL')
        return result

    def _validate_openkh(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('OpenKH location')

        openkh_path = self.openkh_path
        if not openkh_path:
            result.errors.append('OpenKH location not configured in Mods Manager Bridge')
            return result

        if not openkh_path.is_dir():
            result.errors.append('OpenKH location does not exist')
            return result

        result.infos.append('Found OpenKH location [{}]'.format(openkh_path))

        mod_manager_exe_path = openkh_path / 'OpenKh.Tools.ModsManager.exe'
        if not mod_manager_exe_path.is_file():
            result.errors.append('OpenKH location is missing `OpenKh.Tools.ModsManager.exe`')
            return result

        result.infos.append('Found OpenKH Mods Manager executable')

        config_file = openkh_path / 'mods-manager.yml'
        if not config_file.is_file():
            result.errors.append('OpenKH location is missing its configuration file (`mods-manager.yml`)')
            return result

        with open(config_file) as file:
            raw = yaml.safe_load(file)
            game_data_path = path_or_none(raw.get('gameDataPath', ''))

        if not game_data_path:
            result.errors.append('Game Data location not configured in OpenKH Mods Manager')
            return result

        kh2_extract_path = self.games_extract_path / 'kh2'
        if game_data_path != kh2_extract_path:
            result.errors.append(
                'Game data location mismatch between OpenKH Mods Manager [{}] and Mods Manager Bridge [{}]'.format(
                    game_data_path,
                    kh2_extract_path
                )
            )
            return result

        result.infos.append('Game data locations match between OpenKH Mods Manager and Mods Manager Bridge')

        mods_txt_file = openkh_path / 'mods.txt'
        if not mods_txt_file.is_file():
            result.errors.append('OpenKH location is missing `mods.txt` (may not have any mods installed/selected)')
            return result

        with open(mods_txt_file) as file:
            for mod in file:
                result.infos.append('Found mod [{}]'.format(mod.strip()))

        return result

    def _validate_games_extract(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Games Extract location')

        extract_path = self.games_extract_path
        if not extract_path:
            result.errors.append('Games Extract location not configured in Mods Manager Bridge')
            return result

        if not extract_path.is_dir():
            result.errors.append('Games Extract location does not exist')
            return result

        result.infos.append('Found Games Extract location [{}]'.format(extract_path))

        kh2_path = extract_path / 'kh2'
        if not kh2_path.is_dir():
            result.errors.append('Games Extract location does not contain a `kh2` folder')
            return result

        test_path = kh2_path / '00system.bin'
        if not test_path.is_file():
            result.errors.append('Games Extract location is missing some or all extracted KH2 data')
            return result

        result.infos.append('Found extracted KH2 data')
        return result

    def _validate_patches(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Patches location')

        patches_path = self.patches_path
        if not patches_path:
            result.infos.append('Optional Patches location not configured in Mods Manager Bridge')
            return result

        if not patches_path.is_dir():
            result.errors.append('Patches location does not exist')
            return result

        result.infos.append('Found Patches location [{}]'.format(patches_path))

        for file in os.listdir(patches_path):
            if file.endswith('.kh2pcpatch'):
                result.infos.append('Found patch [{}]'.format(file))

        return result

    @staticmethod
    def _validate_lua_scripts() -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Lua scripts')

        home_path = Path(os.path.expanduser('~'))
        default_path = home_path / 'Documents' / 'KINGDOM HEARTS HD 1.5+2.5 ReMIX' / 'scripts' / 'kh2'
        if not default_path.is_dir():
            result.errors.append('Expected script location [{}] does not exist'.format(default_path))
            return result

        result.infos.append('Found script location [{}]'.format(default_path))

        found_scripts = []
        for file in os.listdir(default_path):
            if file.endswith('.lua'):
                found_scripts.append(file)

        if not found_scripts:
            result.errors.append('No Lua scripts were found')
            return result

        for script in found_scripts:
            result.infos.append('Found script [{}]'.format(script))

        return result


class Pcsx2RandoConfiguration:

    def __init__(
            self,
            openkh_path: Optional[Path] = None,
            game_data_path: Optional[Path] = None,
            cheats_path: Optional[Path] = None,
    ):
        self.openkh_path = openkh_path
        self.game_data_path = game_data_path
        self.cheats_path = cheats_path

    @staticmethod
    def read(openkh_path: Optional[Path], cheats_path: Optional[Path]):
        if not openkh_path:
            return Pcsx2RandoConfiguration(openkh_path=openkh_path, cheats_path=cheats_path)

        if not openkh_path.is_dir():
            return Pcsx2RandoConfiguration(openkh_path=openkh_path, cheats_path=cheats_path)

        config_file = openkh_path / 'mods-manager.yml'
        if not config_file.is_file():
            return Pcsx2RandoConfiguration(openkh_path=openkh_path, cheats_path=cheats_path)

        with open(config_file) as file:
            raw = yaml.safe_load(file)
            return Pcsx2RandoConfiguration(
                openkh_path=openkh_path,
                game_data_path=path_or_none(raw.get('gameDataPath', '')),
                cheats_path=cheats_path
            )

    def validate_all(self) -> [ConfigurationCheckResult]:
        return [
            self._validate_openkh(),
            self._validate_games_extract(),
            self._validate_cheats()
        ]

    def _validate_openkh(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('OpenKH location')

        openkh_path = self.openkh_path
        if not openkh_path:
            result.errors.append('OpenKH location not chosen')
            return result

        if not openkh_path.is_dir():
            result.errors.append('OpenKH location does not exist')
            return result

        mod_manager_exe_path = openkh_path / 'OpenKh.Tools.ModsManager.exe'
        if not mod_manager_exe_path.is_file():
            result.errors.append('OpenKH location is missing `OpenKh.Tools.ModsManager.exe`')
            return result

        result.infos.append('Found Mods Manager executable')

        mods_txt_file = openkh_path / 'mods.txt'
        if not mods_txt_file.is_file():
            result.errors.append('OpenKH location is missing `mods.txt` (may not have any mods installed/selected)')
            return result

        with open(mods_txt_file) as file:
            for mod in file:
                result.infos.append('Found mod [{}]'.format(mod.strip()))

        return result

    def _validate_games_extract(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Game Data location')

        extract_path = self.game_data_path
        if not extract_path:
            result.errors.append('Game Data location not configured in OpenKH Mods Manager')
            return result

        if not extract_path.is_dir():
            result.errors.append('Game Data location does not exist')
            return result

        result.infos.append('Found Game Data location [{}]'.format(extract_path))

        test_path = extract_path / '00system.bin'
        if not test_path.is_file():
            result.errors.append('Game Data location is missing some or all extracted KH2 data')
            return result

        result.infos.append('Found extracted KH2 data')
        return result

    def _validate_cheats(self) -> ConfigurationCheckResult:
        result = ConfigurationCheckResult('Cheats location')

        cheats_path = self.cheats_path
        if not cheats_path:
            result.errors.append('Cheats location not chosen')
            return result

        if not cheats_path.is_dir():
            result.errors.append('Cheats location does not exist')
            return result

        result.infos.append('Found Cheats location')

        found_cheats = []
        for file in os.listdir(cheats_path):
            if file.startswith('F266B00B') and file.endswith('.pnach'):
                found_cheats.append(file)

        if not found_cheats:
            result.errors.append('No pnach files were found')
            return result

        for cheat in found_cheats:
            result.infos.append('Found pnach file [{}]'.format(cheat))

        return result


def path_or_none(string: str) -> Optional[Path]:
    if string:
        return Path(string)
    else:
        return None


def path_to_str(path: Optional[Path]) -> str:
    if path is None:
        return ''
    else:
        return str(path)
