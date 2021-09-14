# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 14:36:24 2021

@author: DL67MND
"""
import os
import time
from configobj import ConfigObj
class get_filer():
# =============================================================================
#     
# =============================================================================

    l_list_of_file=[]
    l_list_of_file_POL_TE_FEM=[]
    l_list_of_file_DE_Linux=[]
    l_list_file_to_download=[]
    l_list_of_POL_tree=[]
    def __init__(self, s_Path_Linux_POL, s_Path_Linux_DE):
        self.s_Path_Linux_POL=s_Path_Linux_POL
        self.s_Path_Linux_DE=s_Path_Linux_DE
        
    def f_search_in_file_erfh(self, s_in_file_with_Path):
        """
        

        Parameters
        ----------
        s_in_file_with_Path : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        f_file_in=open(s_in_file_with_Path)
        for line in f_file_in:
            if 'erfh5' in str(line):
                if 'log' in str(line):
                    print('log is not interessin use file')
                else:
                    self.f_cr_fil_to_download(line.rstrip('\n'), self.s_Path_Linux_POL,self.s_Path_Linux_DE)
    
    def m_clean_all_space_to_one(self, string_in):
        string_out=string_in
        while (string_out.find('  ')!=-1):
            string_out=string_in.replace('  ',' ')
            string_in=string_out
        return string_out
    
    def m_clean_space_change_character_to_small(self, string_in):
        """
        Do zrobienia reszte
        """
        string_out=string_in
        string_out=string_in.replace(' ','').lower().replace('_','')
        string_in=string_out
        return string_out
    def m_append_to_array(self, s_tmp_path, tmp_file, s_flag_POL_or_DE):
        f_file_in=open(s_tmp_path + tmp_file)
        i=0
        for line in f_file_in:
            if s_flag_POL_or_DE=='POL':
                self.l_list_of_file_POL_TE_FEM.append(self.m_clean_all_space_to_one(line))
                print(self.l_list_of_file_POL_TE_FEM[i])
                i=i+1
            if s_flag_POL_or_DE=='DE':
                self.l_list_of_file_DE_Linux.append(self.m_clean_all_space_to_one(line))
                print(self.l_list_of_file_DE_Linux[i])
                i=i+1
            if s_flag_POL_or_DE=='POL_TREE':
                self.l_list_of_POL_tree.append(self.m_clean_space_change_character_to_small(line))
                print(self.l_list_of_POL_tree[i])
                i=i+1
    def m_compare_file_without_location(self, s_path_POL_dir,s_DE_login, s_DE_pass, s_DE_IP_Adress, s_Path_Linux_DE):
        i=0
        j=0
        b_Download=False
        for i in range(len(self.l_list_of_file_DE_Linux)):
            print("Linux 1")
            if len(self.l_list_of_file_POL_TE_FEM)==0:
                b_Download=True
            for j in range(len(self.l_list_of_file_POL_TE_FEM)):
                print("Linux 2")
                if os.path.basename(self.l_list_of_file_POL_TE_FEM[j])==os.path.basename(self.l_list_of_file_DE_Linux[i]):
                    print("File was Download :" + os.path.basename(self.l_list_of_file_DE_Linux[i]))
                    b_Download=False
                    break
                else: b_Download=True
            if b_Download==True:
                self.l_list_file_to_download.append(self.l_list_of_file_DE_Linux[i])
                print("File to Download :" + self.l_list_of_file_DE_Linux[i])
                print(os.path.dirname(os.path.abspath(self.l_list_of_file_DE_Linux[i].replace("./","/"))))
                os.system("mkdir -p "+s_path_POL_dir+os.path.dirname(os.path.abspath(self.l_list_of_file_DE_Linux[i].replace("./","/"))))
                #do dodania
                self.m_download_file_from_server(s_DE_login, s_DE_pass, s_DE_IP_Adress, s_Path_Linux_DE, s_path_POL_dir, self.l_list_of_file_DE_Linux[i].replace("./",""))
                #del self.l_list_of_file_POL_TE_FEM[j]
            j=0
    def m_get_all_directory_structur(self, s_Path_Linux_POL, s_tmp_path, tmp_file):
        s_command= "cd "+s_Path_Linux_POL+" ; "+"find . -type "+'"d"'+" > "+ s_tmp_path+tmp_file
        print(s_command)
        os.system(s_command)
        self.m_append_to_array(s_tmp_path, tmp_file, 'POL_TREE')
        
    def f_cr_fil_to_download(self, s_file_name, s_path_in, s_path_out):
        """
        

        Parameters
        ----------
        s_file_name : TYPE
            DESCRIPTION.
        s_path_in : TYPE
            DESCRIPTION.
        s_path_out : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.l_list_of_file.append("get "+s_path_out+s_file_name.replace(" ", "")+" "+s_path_in+s_file_name+'\n')
        print("get "+s_path_out+s_file_name+" "+s_path_out+s_file_name)
    
    def m_get_info_about_file_POL(self, s_Path_Linux_POL, s_tmp_path, tmp_file):
        s_command= "cd "+s_Path_Linux_POL+" ; "+"find . -name "+'"*.fz"'+" -ls >"+ s_tmp_path+tmp_file
        print(s_command)
        os.system(s_command)
        self.m_append_to_array(s_tmp_path, tmp_file, "POL")
    def m_get_info_about_file_DE(self, s_DE_login, s_DE_pass, s_DE_IP_Adress, s_Path_Linux_DE, s_tmp_path, tmp_file):
        #s_command= "sshpass -p '" + s_DE_pass +"' ssh "+s_DE_login + "@" + s_DE_IP_Adress + " 'cd "+s_Path_Linux_DE+" ; "+"find . -name "+'"*.fz"'+" -ls' >" + s_tmp_path + tmp_file
        s_command= "sshpass -p '" + s_DE_pass +"' ssh "+s_DE_login + "@" + s_DE_IP_Adress + " 'cd "+s_Path_Linux_DE+" ; "+"find . -name "+'"*.fz"'+" ' >" + s_tmp_path + tmp_file
        print(s_command)
        os.system(s_command)
        self.m_append_to_array(s_tmp_path, tmp_file, "DE")
    def m_download_file_from_server(self, s_DE_login, s_DE_pass, s_DE_IP_Adress, s_Path_Linux_DE, s_Path_Linux_POL, s_file_to_download):
        #s_command= "sshpass -p '" + s_DE_pass +"' ssh "+s_DE_login + "@" + s_DE_IP_Adress + " 'cd "+s_Path_Linux_DE+" ; "+"find . -name "+'"*.fz"'+" -ls' >" + s_tmp_path + tmp_file
        f = open("get_file_from_Server.txt", "a")
        f.write("get "+s_Path_Linux_DE + s_file_to_download.rstrip("\n") + " " +s_Path_Linux_POL.rstrip("\n") +s_file_to_download.rstrip("\n"))
        f.close()
        s_command= "sshpass -p '" + s_DE_pass +"'  sftp -oBatchMode=no -b "+"get_file_from_Server.txt "+s_DE_login + "@" + s_DE_IP_Adress
        print(s_command)
        os.system(s_command)
        os.remove("get_file_from_Server.txt")
    def f_cr_file_to_sh_download(self, s_out_file_with_Path):
        """
        

        Parameters
        ----------
        s_out_file_with_Path : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        fi_out=open(s_out_file_with_Path,'w')
        for items in self.l_list_of_file:
            fi_out.writelines([items])
        fi_out.close()
    def m_create_ls_file(self, s_Path_to_check, s_name_file):
        with open(s_name_file, "w") as file_object:
            file_object.write("cd "+s_Path_to_check+'\n')
            file_object.write("ls"+'\n')
        file_object.close()
    def m_create_sh_shftp_file_(self, s_DE_login, s_DE_pass, s_DE_IP_Adress, s_CMD_on_sftp_file, s_file_with_log, s_file_name_sh):
        with open(s_file_name_sh, "w") as file_object:
            file_object.write("sshpass -p '" + s_DE_pass +"' sftp -oBatchMode=no -b " +s_CMD_on_sftp_file+" "+s_DE_login+"@"+s_DE_IP_Adress+" > " + s_file_with_log + '\n')
        file_object.close()
class settings_importer():
# =============================================================================
#  Class with settings 
# =============================================================================
        
    def __init__(self, b_create_file): 

        if b_create_file==True:
            config = ConfigObj('FEM_fille_transfer.cfg')
            self.s_Path_Linux_POL= config['Path to listen']['LINUX Path POL']
            self.s_Path_Linux_DE= config['Path to listen']['LINUX Path DE']
            self.s_DE_login=config['Linux DE authorization']['login']
            self.s_DE_pass=config['Linux DE authorization']['password']
            self.s_DE_IP_Adress=config['Linux DE authorization']['IP']
            self.s_type_of_procedur=config['Scheduler']['type of procedure']
            self.s_hour_of_download=config['Scheduler']['Hour of download']
            self.s_minutes_of_download=config['Scheduler']['Minutes of download']
            self.s_tact_in_minutes=config['Scheduler']['Tact in Minutes']
        else:
            self.m_create_config_file()
    def m_create_config_file(self):

        config = ConfigObj()
        config.filename = 'FEM_fille_transfer.cfg'
        #
        config['Path to listen'] = {}
        config['Path to listen']['LINUX Path POL'] = '/te_fem/a0129_ID_BUZZ/40_berechnungen/K23/v106/'
        config['Path to listen']['LINUX Path DE'] = '/net/fem/filer/polkowice/a0129_ID_BUZZ/60_berechnungen/k23/v106/'
        config['Linux DE authorization'] = {}
        config['Linux DE authorization']['login'] = '*******'
        config['Linux DE authorization']['password'] = '*******'
        config['Linux DE authorization']['IP'] = '********'
        
        config.write()

class file_lister_menager():
    def menage_downloade(self):
        ini_Settings=settings_importer(True)
        file_procedure=get_filer(ini_Settings.s_Path_Linux_POL,ini_Settings.s_Path_Linux_DE)
        #s_name_file -> Name of file with ls in directory
        s_name_file="file_with_ls_in_folder.txt"
        file_procedure.m_create_ls_file(ini_Settings.s_Path_Linux_DE, s_name_file)
        s_name_log_file="list_of_file.txt"
        s_ssh_script_name="sh_ls_file_in_sftp.sh"
        file_procedure.m_create_sh_shftp_file_(ini_Settings.s_DE_login, ini_Settings.s_DE_pass, ini_Settings.s_DE_IP_Adress, s_name_file, s_name_log_file, s_ssh_script_name)
        os.system("sh "+s_ssh_script_name)
        file_procedure.f_search_in_file_erfh(s_name_log_file)
        s_name_file="file_to_download.txt"
        s_ssh_script_name="sh_Download_file_from_DE.sh"
        s_name_log_file="log_file.txt"
        file_procedure.f_cr_file_to_sh_download(s_name_file)
        file_procedure.m_create_sh_shftp_file_(ini_Settings.s_DE_login, ini_Settings.s_DE_pass, ini_Settings.s_DE_IP_Adress, s_name_file, s_name_log_file, s_ssh_script_name)
        os.system("sh "+s_ssh_script_name)
    def run_filer(self):
        ini_Settings=settings_importer(True)
        file_procedure=get_filer(ini_Settings.s_Path_Linux_POL,ini_Settings.s_Path_Linux_DE)
        file_procedure.m_get_info_about_file_POL(ini_Settings.s_Path_Linux_POL, "/home/dl67mnd/001_Skrypty/003_FEM_file_Transfer/", "test30032021.txt")
        file_procedure.m_get_info_about_file_DE(ini_Settings.s_DE_login, ini_Settings.s_DE_pass, ini_Settings.s_DE_IP_Adress, ini_Settings.s_Path_Linux_DE, "/home/dl67mnd/001_Skrypty/003_FEM_file_Transfer/", "test_Linux_30032021.txt")
        file_procedure.m_get_all_directory_structur(ini_Settings.s_Path_Linux_POL, "/home/dl67mnd/001_Skrypty/003_FEM_file_Transfer/", "test_structur_POL.txt")
        file_procedure.m_compare_file_without_location(ini_Settings.s_Path_Linux_POL,ini_Settings.s_DE_login, ini_Settings.s_DE_pass, ini_Settings.s_DE_IP_Adress, ini_Settings.s_Path_Linux_DE)
    def mode_one(self):
        self.run_filer()
    def mode_two(self, s_houer, s_minutes):
        licznik = 1
        while 1:
            licznik += 1
            t = time.localtime()
            print(str(time.strftime("%H", t)))
            print(str(time.strftime("%M", t)))
            if str(time.strftime("%H", t))==s_houer and str(time.strftime("%M", t))==s_minutes:
                self.run_filer()
                print("Juz")
                break
    def mode_three(self, in_tact):
        while 1:
            time.sleep(float(in_tact) * 60)
            self.run_filer()
    def operating_mode(self):
        ini_Settings=settings_importer(True)
        if ini_Settings.s_type_of_procedur=="1":
            self.mode_one()
        elif ini_Settings.s_type_of_procedur=="2":
            self.mode_two(ini_Settings.s_hour_of_download,ini_Settings.s_minutes_of_download)
        elif ini_Settings.s_type_of_procedur=="3":
            self.mode_three(ini_Settings.s_tact_in_minutes)
        else :
            print("Sprawdz poprawnosc pliku ini")
def main():
    #Settings_test=settings_importer(False)
    menage_run=file_lister_menager()
   #odhashowac pozniej menage_run.menage_downloade()
    menage_run.operating_mode()
if __name__ == '__main__':
    main()