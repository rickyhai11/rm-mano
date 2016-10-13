
import pbr.version

PLAYNETMANO_RM_VENDOR = "Rickyhai"
PLAYNETMANO_RM_PRODUCT = "Playnetmano_rm"
PLAYNETMANO_RM_PACKAGE = None  # OS distro package version suffix

version_info = pbr.version.VersionInfo('playnetmano_rm')
version_string = version_info.version_string


def vendor_string():
    return PLAYNETMANO_RM_VENDOR


def product_string():
    return PLAYNETMANO_RM_PRODUCT


def package_string():
    return PLAYNETMANO_RM_PACKAGE


def version_string_with_package():
    if package_string() is None:
        return version_info.version_string()
    else:
        return "%s-%s" % (version_info.version_string(), package_string())
