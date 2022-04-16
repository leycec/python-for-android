import sh
from os.path import join
from pythonforandroid.recipe import PythonRecipe
from pythonforandroid.toolchain import shprint, info

# Lightly inspired by Bleak's upstream p4a recipe residing at:
#     https://github.com/hbldh/bleak/blob/develop/bleak/backends/p4android/recipes/bleak/__init__.py
class BleakRecipe(PythonRecipe):
    version = '0.14.2'
    url = 'https://pypi.python.org/packages/source/b/bleak/bleak-{version}.tar.gz'
    name = 'bleak'
    blake2bsum = '9a6adb9ec627248255586d53260648cfdb2e6054b0faa4a35b92138f8a87a8b7bcff14f4e84a45b931ad13880d37a6de7ac2174235d6df38b0758442ca2da105'
    sha512sum = '5594e5ac524fb8969c16202b7984c546daf65c7d2492df7bf2cefbcf1839dfdc0cb8ca0c0304722b9a85bb9110b08625c0f15626a0139634fb0162e7e1fd0dbb'

    depends = ['pyjnius', 'setuptools']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch=None, with_flags_in_cc=True):
        env = super().get_recipe_env(arch, with_flags_in_cc)
        env['PYJNIUS_PACKAGES'] = self.ctx.get_site_packages_dir(arch)
        return env

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)

        info('Copying Java class files...')
        src_javaclass_dir = join(
            self.get_build_dir(arch.arch),
            'bleak', 'backends', 'p4android', 'java',
        )
        shprint(sh.cp, '-a', src_javaclass_dir, self.ctx.javaclass_dir)


recipe = BleakRecipe()
