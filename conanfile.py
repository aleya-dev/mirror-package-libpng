from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMakeDeps
from conan.tools.files import rmdir, rm, collect_libs
import os


required_conan_version = ">=2.0"


class LibPngConan(ConanFile):
    name = "libpng"
    version = "1.6.40"
    python_requires = "aleya-conan-base/1.3.0@aleya/public"
    python_requires_extend = "aleya-conan-base.AleyaCmakeBase"
    ignore_cpp_standard = True

    exports_sources = "source/*"

    options = {
        "shared": [False, True],
        "fPIC": [False, True]
    }

    default_options = {
        "shared": False,
        "fPIC": True
    }

    requires = "zlib/1.3.0@aleya/public"

    def configure(self):
        super().configure()

        self.options["zlib"].shared = self.options.shared

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["CMAKE_DEBUG_POSTFIX"] = ''
        tc.variables["PNG_TESTS"] = False
        tc.variables["PNG_EXECUTABLES"] = False
        tc.variables["PNG_SHARED"] = self.options.shared
        tc.variables["PNG_STATIC"] = not self.options.shared
        tc.generate()
        tc = CMakeDeps(self)
        tc.generate()

    def package(self):
        super().package()

        rmdir(self, os.path.join(self.package_folder, "share"))
        rmdir(self, os.path.join(self.package_folder, "lib", "pkgconfig"))

        if self.options.shared:
            rm(self, "*.a", os.path.join(self.package_folder, "lib"), recursive=True)
        else:
            rm(self, "*.so", os.path.join(self.package_folder, "lib"), recursive=True)
            rmdir(self, os.path.join(self.package_folder, "bin"))

        rm(self, "*.cmake", os.path.join(self.package_folder, "lib"), recursive=True)

    def package_info(self):
        self.cpp_info.set_property("cmake_find_mode", "both")
        self.cpp_info.set_property("cmake_file_name", "PNG")
        self.cpp_info.set_property("cmake_target_name", "PNG::PNG")
        self.cpp_info.set_property("pkg_config_name", "libpng")

        self.cpp_info.libs = collect_libs(self)
