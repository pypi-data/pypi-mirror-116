from retro_data_structures.conversion.asset_converter import AssetConverter, Resource, AssetDetails
from retro_data_structures.conversion.errors import UnsupportedTargetGame, UnsupportedSourceGame
from retro_data_structures.game_check import Game


def find_missing(lst):
    return [x for x in range(lst[0], lst[-1] + 1)
            if x not in lst]


def convert_from_prime(data: Resource, details: AssetDetails, converter: AssetConverter):
    if converter.target_game != Game.ECHOES:
        raise UnsupportedTargetGame(Game.PRIME, converter.target_game)

    # ====================

    bones = {}

    for i, it in enumerate(data["anim"]["bone_channel_descriptors"]):
        bones[i] = it["bone_id"]

    for i, it in enumerate(find_missing(sorted(bones.values()))):
        data["anim"]["bone_channel_descriptors"].append({
            "bone_id": it,
            "rotation_keys_count": 0,
            "rotation_keys": None,
            "translation_keys_count": 0,
            "translation_keys": None,
            "scale_keys_count": None,
            "scale_keys": None,
        })

        for key in data["anim"]["animation_keys"]:
            if key["channels"] is not None:
                key["channels"] += [{"rotation": None, "translation": None, "scale": None}]

    old = data["anim"]["bone_channel_descriptors"]
    data["anim"]["bone_channel_descriptors"] = [None] * (len(old))
    index_conversion = {}
    for i, it in enumerate(old):
        new_bone_id = it["bone_id"] - 3
        it["bone_id"] = new_bone_id
        it["scale_keys_count"] = 0
        data["anim"]["bone_channel_descriptors"][new_bone_id] = it
        index_conversion[new_bone_id] = i

    for key in data["anim"]["animation_keys"]:
        if key["channels"] is not None:
            key["channels"] = [
                key["channels"][index_conversion[i]]
                for i, _ in enumerate(key["channels"])
            ]

    data["anim"]["scale_multiplier"] = 0.0
    data["anim"]["event_id"] = None
    data["anim"]["root_bone_id"] = data["anim"]["root_bone_id"] - 3
    data["anim"]["unk_1"] = None
    data["anim"]["unk_2"] = 0x0101  # Always 0x0101 in MP2

    return data


def convert_from_echoes(data: Resource, details: AssetDetails, converter: AssetConverter):
    if converter.target_game != Game.PRIME:
        raise UnsupportedTargetGame(Game.ECHOES, converter.target_game)

    old = data["anim"]["bone_channel_descriptors"]
    data["anim"]["bone_channel_descriptors"] = [None] * len(old)
    index_conversion = {}
    for i, it in enumerate(old):
        new_bone_id = it["bone_id"] + 3
        it["bone_id"] = new_bone_id
        it["scale_keys_count"] = None
        data["anim"]["bone_channel_descriptors"][i] = it
        index_conversion[new_bone_id] = i

    enumme = data["anim"]["bone_channel_descriptors"].copy()
    remove_count = 0
    for i, bcd in enumerate(enumme):
        if bcd["translation_keys_count"] == 0 and bcd["scale_keys_count"] is None and bcd["rotation_keys_count"] == 0:
            del index_conversion[data["anim"]["bone_channel_descriptors"][i - remove_count]["bone_id"]]
            del data["anim"]["bone_channel_descriptors"][i - remove_count]
            remove_count += 1

    for key in data["anim"]["animation_keys"]:
        if key["channels"] is not None:
            enumme = key["channels"].copy()
            remove_count = 0
            for i, channel in enumerate(enumme):
                if channel["rotation"] is None and channel["translation"] is None and channel["scale"] is None:
                    del key["channels"][i - remove_count]
                    remove_count += 1

    data["anim"]["scale_multiplier"] = None

    # FIXME - Must create new asset ID for EVNT parsed from corresponding ANCS and assign here
    data["anim"]["event_id"] = 0xFFFFFFFF

    data["anim"]["root_bone_id"] = data["anim"]["root_bone_id"] + 3
    data["anim"]["unk_1"] = 1
    data["anim"]["unk_2"] = None

    return data


def convert_from_corruption(data: Resource, details: AssetDetails, converter: AssetConverter):
    raise UnsupportedSourceGame(Game.CORRUPTION)


CONVERTERS = {
    Game.PRIME: convert_from_prime,
    Game.ECHOES: convert_from_echoes,
    Game.CORRUPTION: convert_from_corruption,
}
