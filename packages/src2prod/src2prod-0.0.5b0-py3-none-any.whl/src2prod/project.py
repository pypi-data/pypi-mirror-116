#! /usr/bin/env python3

###
# This module implements all the logic needed to manage one project.
###


from shutil import rmtree

from spkpb import *

from .baseproj import *


# ------------------------ #
# -- PROJECT MANAGEMENT -- #
# ------------------------ #

###
# This class is the main one to use such as to easily manage a project 
# following the "source-to-final-product" workflow.
###

class Project(BaseProj):
###
# prototype::
#     safemode = ( True ) ; // See Python typing...
#                ``True`` asks to never remove a none empty target folder
#                contrary to ``False``.
#
# info::
#     The argument ``safemode`` is here to leave the responsability of
#     removing a none empty folder to the user (my lawyers forced me to
#     make that choice).
###
    def update(self, safemode: bool = True) -> None:
# Say "Hello!".
        self._start_one_session(
            title       = f'"{self.project.name}": UPDATE',
            timer_title = 'update'
        )

# Build the l.o.f.
        self.build(
            opensession  = False,
            closesession = False,
        )

        if not self.success:
            self._close_one_session(timer_title = 'update')
            return

# Safe mode?
        if (
            safemode
            and
            not self.isempty(self.target)
        ):
            self.new_error(
                what = self.target,
                info = (
                    'target folder exists and is not empty '
                    '(safe mode used).'
                )
            )

            self._close_one_session(timer_title = 'update')

            return

# We can update the target folder. 
        for name in [
            'empty_target',
            'copy_src2target',
            'copy_readme',
        ]:
            getattr(self, name)()

# Every copies has been made.
        self.recipe(
            {VAR_STEP_INFO: 
                f'Target folder updated.'}
        )

# Say "Good bye!".
        self._close_one_session(timer_title = 'update')

###
# This method creates or empties the target folder.
###
    def empty_target(self) -> None:
# The target folder must be deletted.
        if self.target.is_dir():
            action = 'emptied'

            rmtree(self.target)

        else:
            action = 'created'

# Create a new version of the target folder.
        self.target.mkdir()

# We are so happy to talk about our exploit...
        self.recipe(
            {VAR_STEP_INFO: 
                f'Target folder has been {action}:'
                 '\n'
                f'"{self.target}".'},
        )

###
# This method copies the files kept from the source to the target.
###
    def copy_src2target(self) -> None:
# Indicating the start of the copying.
        nb_files = len(self.lof)
        plurial  = '' if nb_files == 1 else 's'

        self.recipe(
            {VAR_STEP_INFO: 
                f'Copying {nb_files} file{plurial} from source to target.'}
        )

# Let's copy each files.
        for srcfile in self.lof:
            targetfile = self.target / srcfile.relative_to(self.source)

            self.copyfile(
                source = srcfile,
                target = targetfile
            )

###
# This method copies an external path::``README`` file if it is necessary.
###
    def copy_readme(self) -> None:
# No README to copy.
        if self.readme is None:
            return

# Just copy the external README.
        readme_rel = self.readme.relative_to(self.project)

        self.copyfile(
            source = self.readme,
            target = self.target / self.readme.name
        )
        
        self.recipe(
            {VAR_STEP_INFO: 
                f'"{readme_rel}" added to the target.'}
        )


###
# prototype::
#     opensession  = ; // See Python typing...
#                    ``True`` is to reset eveything and open the communication 
#                    and ``False`` starts directly the work.
#     closesession = ; // See Python typing...
#                    ``True`` is to close the communication and 
#                    ``False`` otherwise.
#              
#
# This method is the great bandleader building the list of files to be copied to
# the target dir.
###
    def build(
        self,
        opensession : bool = True,
        closesession: bool = True,
    ) -> None:
# Do we close the session?
        if opensession:
            self._start_one_session(
                title       = f'"{self.project.name}": LIST OF FILES',
                timer_title = 'build'
            )

# List of methods called.
        methodenames = [
            'check_readme',
            'build_ignore',
        ]

        if self.usegit:
            methodenames.append('check_git')

        methodenames.append('files_without_git')

        if self.usegit:
            methodenames.append('removed_by_git')

# Let's work.
        for name in methodenames:
            getattr(self, name)()

            if not self.success:
                break

# Do we close the session?
        if closesession:
            self._close_one_session(timer_title = 'build')


###
# This method checks the existence of a path::``README`` file if the user
# has given suche one.
###
    def check_readme(self) -> None:
# No external README.
        if self.readme is None:
            return

# An external README.
        if not self.readme.is_file():
            self.new_error(
                what  = self.readme,
                info  = '"README" file not found.',
                level = 1
            )
            return

        self.recipe(
            {VAR_STEP_INFO: 
                 'External "README" file to use:'
                 '\n'
                 f'"{self.readme}".'}
        )


###
# This method does three things.
#
#     1) Indirecty it checks that ¨git can be used.   
#     2) It finds the branch on which we are working.
#     3) It verifies that there isn't any uncommitted changes in the source files.
#
# warning::
#     We do not want any uncommitted changes even on the ignored files because this
#     could imply some changes in the final product. 
###
    def check_git(self) -> None:
        self.recipe(
            {VAR_STEP_INFO: f'Checking "git".'}
        )

# Let's go
        infos = {}

        for kind, options in [
# Current branch.
            ('branch', ['branch']),
# We don't want uncommitted files in our source folder!
            ('uncommitted', ['a']),
        ]:
            infos[kind] = self.rungit(options)
    
            if not self.success:
                return

# Branch used.
        for onebranch in infos['branch'].split('\n'):
            if onebranch.startswith('*'):
                branch = onebranch[1:].strip()
                break

        self.recipe(
            {VAR_STEP_INFO: f'Working in the branch "{branch}".'}
        )

# Uncommitted changes in our source?
        tosearch = f'{self.project.name}/{self.source.name}/'

        if (
            "Changes to be committed" in infos['uncommitted']
            and
            tosearch in infos['uncommitted']
        ):
            gitinfos = [
                x.strip()
                for x in infos['uncommitted'].split('\n')
                if tosearch in x
            ]

            nb_changes = len(gitinfos)
            howmany    = 'one' if nb_changes == 1 else 'several'
            plurial    = ''    if nb_changes == 1 else 's'

            if len(gitinfos) <= 5:
                whichuncommitted = ''

            else:
                whichuncommitted = ' the 5 first ones'
                gitinfos         = gitinfos[:5] + '...'

            fictive_tab = '\n    + '
            gitinfos    = fictive_tab.join()

            self.new_error(
                what = self.source,
                info = (
                    f'{howmany} uncommitted file{plurial} found in the source folder. '
                    f'See{whichuncommitted} below.'
                    f'{fictive_tab}{gitinfos}'
                ),
                level = 1
            )
            return


###
# This method builds the list of files to keep just by using the ignore rules.
#
# info::
#     ¨git is not used here.
###
    def files_without_git(self) -> None:
# Let's talk.
        self.recipe(
            {VAR_STEP_INFO: 
                 'Starting the analysis of the source folder:'
                 '\n'
                f'"{self.source}".'},
        )

# Does the source dir exist?
        if not self.source.is_dir():
            self.new_error(
                what = self.source,
                info = 'source folder not found.',
            )
            return

# List all the files.
        self.lof = [
            f for f in self.iterfiles(self.source)
        ]

# An empty list stops the process.
        if not self.lof:
            self.new_critical(
                what = self.source,
                info = 'empty source folder.',
            )
            return

# Let's be proud of our 1st list.
        if self.usegit:
            whatused = 'the rules from "ignore"'
        
        else:
            whatused = 'only the rules from "ignore"'

            self._indicating_lof_found(
                output   = FORLOG,
                whatused = whatused
            )

        self._indicating_lof_found(
            output   = FORTERM,
            whatused = whatused
        )


###
# This method shrinks the list of files by using the ignore rules used by ¨git.
#
# info::
#     The method ``rungit`` fails with ``options = ['check-ignore', '**/*'])``, 
#     so we must test directly each path.
###
    def removed_by_git(self) -> None:
        len_lof_before = len(self.lof)

# Let's talk.
        self.recipe(
            FORTERM,
                {VAR_STEP_INFO: 
                    'Removing unwanted files using "git".'},
        )

        self.lof = [
            onefile
            for onefile in self.lof
            if not self.rungit(
                options = [
                    'check-ignore',
                    onefile.relative_to(self.project)
                ]
            )
        ]
        
# Let's be proud of our 2nd list.
        len_lof = len(self.lof)
        
        if len_lof_before == len_lof:
            extra = ' No new file ignored.'

        else:
            nb_new_ignored = len_lof_before - len_lof
            plurial        = '' if nb_new_ignored == 1 else 's'

            extra = (
                f' {nb_new_ignored} new file{plurial} '
                 'ignored thanks to "git".'
            )

        self._indicating_lof_found(
            output   = FORTERM,
            whatused = '"git"',
            extra    = extra
        )

        self._indicating_lof_found(
            output   = FORLOG,
            whatused = '"git" and the rules from "ignore"',
        )


###
# prototype::
#     output   = _ in [FORTERM, FORLOG, FORALL]; // See Python typing...
#                the output(s) where we want to communicate.
#     whatused = ; // See Python typing...
#                the method used to shrink the list of files.
#     extra    = ( '' ); // See Python typing...
#                a small extra text.
#
# This method is just a factorization.
###
    def _indicating_lof_found(
        self,
        output  : str,
        whatused: str,
        extra   : str = ''
    ) -> None: 
        len_lof = len(self.lof)
        plurial = '' if len_lof == 1 else 's'

        self.recipe(
            output,
                {VAR_STEP_INFO: 
                    f'{len_lof} file{plurial} found using {whatused}.{extra}'},
        )


###
# prototype::
#     title       = ; // See Python typing...
#                   the title of the session.
#     timer_title = ; // See Python typing...
#                   the title for the time stamp.
#
# This method is just a factorization.
###
    def _start_one_session(
        self, 
        title      : str,
        timer_title: str
    ) -> None:
        self.reset()
        
        self.timestamp(f'{timer_title} - start')
        
        self.recipe(
                {VAR_TITLE: title},
            FORTERM,
                {VAR_STEP_INFO: 
                     'The log file used will be :'
                     '\n'
                    f'"{self.logfile}".'},
        )

###
# prototype::
#     timer_title = ; // See Python typing...
#                   the title for the time stamp.
#
# This method is just a factorization.
###
    def _close_one_session(
        self, 
        timer_title: str
    ) -> None:
        self.resume()
        
        self.recipe(
            FORLOG,
                NL
        )
        
        self.timestamp(f'{timer_title} - end')
