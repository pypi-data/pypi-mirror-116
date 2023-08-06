#! /usr/bin/env python3

###
# This module is just a factorization gathering all the technical and stupid
# methods.
###


from shutil import copyfile
from subprocess import run

from spkpb import *


# ------------------------------------------------------- #
# -- TECHNICAL CLASS ABSTRACTION FOR LOW LEVEL ACTIONS -- #
# ------------------------------------------------------- #

###
# This class contains technical methods used by the class ``project.Project``.
###

class LowLevel(BaseCom):
    DIR_TAG  = 'dir'
    FILE_TAG = 'file'

###
# prototype::
#     project = ; // See Python typing...
#               the folder project that will be used to communicate during 
#               the analysis.
#     source  = ; // See Python typing...
#               the **relative** path of the source dir (regarding the project
#               folder).
#     target  = ; // See Python typing...
#               the **relative** path of the final product dir (regarding the
#               project folder).
#     ignore  = ( '' ) ; // See Python typing...
#               the ¨gitingore like rules for ignoring files in addition to what
#               ¨git does. You can use this argument even if you don't work with 
#               ¨git.
#     usegit  = ( False ) ; // See Python typing...
#               ''True'' asks to use ¨git contrary to ``False``.
#     readme  = ( None ) ; // See Python typing...
#               ''None'' is if you don't need to import an external 
#               path::``README`` file, otherwise give a **relative** path.
#
# warning::
#     The target folder is totally removed and reconstructed at each new
#     update.
#
# info::
#     Additional attributes are created/reseted by the method ``reset``.
###
    def __init__(
        self,
        project: Union[str, Path],
        source : Union[str, Path],
        target : Union[str, Path],
        ignore : str                    = '',
        usegit : bool                   = False,
        readme : Union[None, str, Path] = False,
    ):
# To communicate.
        self.logfile = project / f'{project.name}.src2prod.log'

        super().__init__(
            Problems(
                Speaker(
                    logfile = self.logfile,
                    style   = GLOBAL_STYLE_COLOR,
                )
            )
        )

# User's choices.
        self.project = self.pathify(project)
        self.source  = self.project / self.pathify(source)
        self.target  = self.project / self.pathify(target)

        self.usegit  = usegit
        
        self.build_ignore(ignore)

        if not readme is None:
            readme = self.project / self.pathify(readme)

        self.readme = readme


###
# prototype::
#     value = ; // See Python typing...
#             a path.
#
#     :return: = ; // See Python typing...
#                the path converted to an instance of ``pathlib.Path``.
###
    def pathify(self, value: Union[str, Path]) -> Path:
        valtype = type(value)

        if valtype == str:
            value = Path(value)

        elif not isinstance(value, Path):
            raise ValueError(
                f'type {valtype} unsupported to indicate '
                 'the source and the target.'
            )

        return value


###
# prototype::
#     :see: = spkpb.problems.Problems.reset
#
# This method resets everything.
###
    def reset(self) -> None:
        super().reset()

        self.recipe(
            FORLOG,
                {VAR_TITLE: 
                    f'"{self.project.name}": SOURCE --> FINAL PRODUCT'},
        )

# Extra attributs.    
        self.success         = True
        self.lof: List[Path] = []


###
# prototype::
#     ignore = ; // See Python typing...
#              the ``gitignore`` like rules.
#
# This method builds ``self.ignore`` which is a dictinnary looking like
# the following one.
#
# python::
#     {
#         self.DIR_TAG : [
#             rule_1_to_ignore_some_dirs,
#             rule_2_to_ignore_some_dirs,
#             ...
#         ],
#         self.FILE_TAG : [
#             rule_1_to_ignore_some_files,
#             rule_2_to_ignore_some_files,
#             ...
#         ],
#     }
###
    def build_ignore(self, ignore: str) -> None:
        self.ignore = {
            self.DIR_TAG : [],
            self.FILE_TAG: [],
        }

        for rule in ignore.split('\n'):
            if not(shortrule := rule.strip()):
                continue

# A dir rule.
            if shortrule.endswith('/'):
                context   = self.DIR_TAG
                shortrule = shortrule[:-1]

# A file rule.
            else:
                context = self.FILE_TAG
            
            self.ignore[context].append(shortrule)

###
# prototype::
#     fileordir = ; // See Python typing...
#                 the path of a file or a dir.
#     kind      = _ in [self.DIR_TAG, self.FILE_TAG]; // See Python typing...
#                 the kind of ¨io object.
#
#     :return: = ; // See Python typing...
#                ``True`` if the ¨io object must be kept regarding the ignore
#                 rules, and ``False`` otherwise.
#
# info::
#     ¨git is not used here.
###
    def keepthis(
        self,
        fileordir: Path,
        kind     : str
    ) -> bool:            
        for onerule in self.ignore[kind]:
            if fileordir.match(onerule):
                return False

        return True

###
# prototype::
#     onedir = ; // See Python typing...
#              a dir to analyze.
#
#     :yield: = ; // See Python typing...
#               the files in the folder ``onedir`` kept after the application 
#               of the ignore rules.
#
# info::
#     ¨git is not used here.
###
    def iterfiles(self, onedir: Path) -> Path:
        for fileordir in onedir.iterdir():
            if fileordir.is_dir():
                if self.keepthis(
                    fileordir = fileordir,
                    kind      = self.DIR_TAG
                ):
                    for onefile in self.iterfiles(onedir = fileordir):
                        yield onefile

            elif self.keepthis(
                fileordir = fileordir,
                kind      = self.FILE_TAG
            ):
                yield fileordir


###
# prototype::
#     onedir = ; // See Python typing...
#              a dir.
#
#     :return: = ; // See Python typing...
#                ``True`` if the folder doesn't exist yet or is empty and
#                ``False`` otherwise.
###
    def isempty(self, onedir: Path) -> bool:
# The folder doesn't exist.
        if not onedir.is_dir():
            return True

# Does the folder contain something?
        nothingfound = True

        for _ in onedir.iterdir():
            nothingfound = False
            break

# The job has been done.
        return nothingfound


###
# prototype::
#     source = ; // See Python typing...
#              the path of the source file to copy.
#     target = ; // See Python typing...
#              the path of the target file that will be the copy.
###
    def copyfile(
        self,
        source: Path,
        target: Path,
    ) -> None:
        target.parent.mkdir(
            parents  = True,
            exist_ok = True
        )

        copyfile(source, target)


###
# prototype::
#     options = ; // See Python typing...
#              a list of options.
#
#     :return: = ; // See Python typing...
#                the stripped standard output sent by the command.
#
# This method launches the command terminal::``git`` with the options given
# in the list ``options``.
###
    def rungit(self, options: List[str]) -> str:
        cmd = ['git'] + options

# Launch the command in the project folder.
        try:
            output = run(
                cmd, 
                capture_output = True,
                cwd            = self.project
            )

# Can't launch the command.
        except FileNotFoundError as e:
            cmd = " ".join(cmd)
    
            self.new_error(
                what = self.source,
                info = f'can\'t use "{cmd}".',
            )
            return

# Command launched throws an error.
        if output.stderr:
            self.new_error(
                what = self.source,
                info = (
                    f'error throwed by "{cmd}":'
                     '\n'
                    f'"{self.decode(output.stderr)}".'
                ),
            )
            return

# The work has been done correctly.
        return self.decode(output.stdout).strip()

###
# prototype::
#     bytedatas = ; // See Python typing...
#                 a byte content.
#
#     :return: = ; // See Python typing...
#                the string obtained by decoding with the ¨utf8 encoding.
###
    def decode(self, bytedatas: bytes) -> str:
        return bytedatas.decode('utf-8')