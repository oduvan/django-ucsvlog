import os
import time

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from djucsvlog.glog import glog
import djucsvlog.settings as my_settings
from ucsvlog.log_decorators import a_log_call


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
                make_option('--folder',
                            dest='folder',
                            default = my_settings.CLEAR_OLD_FOLDER,
                            help='path to the folder, which has to be inspect'
                            ),
                make_option('--perion',
                            dest='period',
                            default = my_settings.CLEAR_OLD_PERIOD,
                            help='period of old logs'
                            ),
                make_option('--remove',
                            dest='remove_files',
                            action='store_true',
                            default = False,
                            help='period of old logs'
                            ),
                make_option('--archive',
                            dest='archive_mask',
                            default = my_settings.CLEAR_OLD_ARCHIVE,
                            help='archive mask'
                            ),
                        )

    period_sec = None # calculated value of period. From days to sec
    filtered_files = None # array of file abs name which has to be clear
    abs_folder = None # absolute folder for logs clear


    @a_log_call(glog)
    def handle(self,folder,period, remove_files, archive_mask, *args,**kwargs):
        self.period_sec = period * 24 * 60 * 60
        self.filtered_files = []

        if folder:
            folder = os.path.abspath(folder)
        else:
            assert my_settings.FILE, 'You have to defile folder attr, settings.UCSVLOG_CLEAR_OLD_FOLDER or UCSVLOG_FILE'

            #getting search folder from FILE settings
            abs_folder = os.path.abspath(my_settings.FILE)
            abs_folder_els = []
            for el in abs_folder.split('/')[1:]:
                if  el.find('%') + 1:
                    break
                abs_folder_els.append(el)
            folder = '/' + '/'.join(abs_folder_els)

        self.abs_folder = folder

        os.path.walk(folder,self.walk_directory,None)
        if not self.filtered_files:
            glog.log('nothing to do')
            return

        if remove_files:
            self.remove_filtered_files()
            return

        if archive_mask:
            self.archive_filtered_files(archive_mask)
            self.remove_filtered_files()
            return


    def remove_filtered_files(self):
        for item in self.filtered_files:
            glog.log(['unlink',item])
            #os.unlink(item)

    def archive_filtered_files(self,archive_mask):
        import tarfile
        def reset_abs_folder(tarinfo, abs_folder = self.abs_folder):
            tarinfo.name = tarinfo.name[len(abs_folder):]
            return tarinfo
        tar = tarfile.open(archive_mask % glog.action_log_template_params(), "w:gz")
        for item in self.filtered_files:
            tar.add(item, filter=reset_abs_folder)
        tar.close()





    def walk_directory(self,args,dirname,names):
        for filename in names:
            full_name = os.path.join(dirname, filename)
            if not os.path.isfile(full_name):
                continue
            if ( time.time() - os.path.getctime(full_name) ) > self.period_sec:
                glog.log(['walk',full_name,'Y'])
                self.filtered_files.append(full_name)
            else:
                glog.log(['walk',full_name,'N'])
