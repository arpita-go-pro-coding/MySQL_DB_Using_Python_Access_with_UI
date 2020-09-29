from db_page import *
from mysql_login import *
from table_page import *
from table_info_page import *

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox,QTableWidgetItem

import mysql.connector

class MySqlDatabase:

    def __init__(self,my_window):

        self.mysql_login_page = Ui_Mysql_Window()
        self.mysql_window = QtWidgets.QMainWindow()
        self.mysql_login_page.setupUi(self.mysql_window)

        self.db_page = Ui_MainWindow()
        self.db_window = QtWidgets.QMainWindow()
        self.db_page.setupUi(self.db_window)

        self.table_page = Ui_Table_MainWindow()
        self.table_window = QtWidgets.QMainWindow()
        self.table_page.setupUi(self.table_window)

        self.table_info_page=Ui_Table_Info_MainWindow()
        self.table_info_window=QtWidgets.QMainWindow()
        self.table_info_page.setupUi(self.table_info_window)


        ## MySQL Login Page
        self.mysql_login_page.uname_lineEdit.textChanged.connect(self.activate_password_line_edit)
        self.mysql_login_page.paswd_lineEdit.textChanged.connect(self.activate_host_line_edit)
        self.mysql_login_page.hname_lineEdit.textChanged.connect(self.activate_port_line_edit)
        self.mysql_login_page.port_lineEdit.textChanged.connect(self.activate_check_con_button)

        self.mysql_login_page.check_con_pushButton.clicked.connect(self.check_connectivity)
        self.mysql_login_page.reset_pushbutton.clicked.connect(self.reset_fields)
        self.mysql_login_page.login_pushButton.clicked.connect(self.access_db_page)

        ## DB Page
        self.db_page.back_pushButton.clicked.connect(self.handle_back_db_window)
        self.db_page.show_db_pushButton.clicked.connect(self.show_databases)
        self.db_page.reset_db_pushButton.clicked.connect(self.reset_db_page_fields)
        self.db_page.db_list_comboBox.textActivated.connect(self.activate_next_db_window)
        self.db_page.next_pushButton.clicked.connect(self.access_table_page)

        ## Table Page
        self.table_page.back_in_table_pushButton.clicked.connect(self.handle_back_table_window)
        self.table_page.show_in_table_pushButton.clicked.connect(self.show_tables)
        self.table_page.reset_in_table_pushButton.clicked.connect(self.reset_table_page_fields)
        self.table_page.table_list_comboBox.textActivated.connect(self.activate_next_table_window)
        self.table_page.next_in_tablepage_pushButton.clicked.connect(self.access_table_info_page)

        ## Table Info Page
        self.table_info_page.back_in_table_info_pushButton.clicked.connect(self.handle_back_table_info_window)
        self.table_info_page.show_count_in_table_info_pushButton.clicked.connect(self.show_record_count)
        self.table_info_page.desc_table_in_table_info_pushButton.clicked.connect(self.desc_table)


    ### MySQL Login Page

    def my_sql_login_initial_load(self):
        """Disable buttons and text boxes when MySQL Window loads"""

        self.mysql_login_page.check_con_pushButton.setEnabled(False)
        self.mysql_login_page.reset_pushbutton.setEnabled(False)
        self.mysql_login_page.login_pushButton.setEnabled(False)

        self.mysql_login_page.paswd_lineEdit.setEnabled(False)
        self.mysql_login_page.hname_lineEdit.setEnabled(False)
        self.mysql_login_page.port_lineEdit.setEnabled(False)



    def display_mysql_window(self):
        """Show MySQL Login Window"""
        self.my_sql_login_initial_load()
        self.mysql_window.show()


    def activate_password_line_edit(self):
        """Activate the password line edit"""
        self.mysql_login_page.paswd_lineEdit.setEnabled(True)
        self.mysql_login_page.reset_pushbutton.setEnabled(True)

    def activate_host_line_edit(self):
        """Activate host line edit"""
        self.mysql_login_page.hname_lineEdit.setEnabled(True)
        self.mysql_login_page.reset_pushbutton.setEnabled(True)

    def activate_port_line_edit(self):
        """Activate port line edit"""
        self.mysql_login_page.port_lineEdit.setEnabled(True)
        self.mysql_login_page.reset_pushbutton.setEnabled(True)

    def get_credentials_from_user(self):
        """Get the user credentials to connect to db"""
        user_input=self.mysql_login_page.uname_lineEdit.text()
        password_input=self.mysql_login_page.paswd_lineEdit.text()
        host_input=self.mysql_login_page.hname_lineEdit.text()
        port_input=self.mysql_login_page.port_lineEdit.text()

        return user_input, password_input, host_input, port_input

    def activate_check_con_button(self):
        """Activate Check Connectivity push button"""
        self.mysql_login_page.check_con_pushButton.setEnabled(True)

    @staticmethod
    def create_db_connection():
        """Create db connection"""
        con = mysql.connector.connect(user='root', password='pihul', host='localhost', port=3306)
        return con

    def check_connectivity(self):
        """Check connection whether it is successful or not"""

        # user = self.get_credentials_from_user()[0]
        # password = self.get_credentials_from_user()[1]
        # host = self.get_credentials_from_user()[2]
        # port = self.get_credentials_from_user()[3]

        user = 'root'
        password = 'pihul'
        host = 'localhost'
        port = str(3306)
        try:

            if user == 'root' and password == 'pihul' and host == 'localhost' and port == str(3306):
                try:
                    con_obj=MySqlDatabase.create_db_connection()
                    if con_obj.is_connected():
                        self.test_success_popup()

                except Exception as e:
                    print("Unable to connect to database, with exception msg:", e)

                finally:
                    con_obj.close()

            else:
                self.invalid_cred_popup()

        except Exception as e1:
            print("Connectivity issue...please check, with except msg:", e1)

    def user_blank_popup(self):
        """User name field is blank or not"""
        uname_blank_msg = QMessageBox()
        uname_blank_msg.setWindowTitle("Connection Failed")
        uname_blank_msg.setText("User name can't be blank!!! ")
        uname_blank_msg.setIcon(QMessageBox.Critical)
        x = uname_blank_msg.exec_()

    def invalid_cred_popup(self):
        """Invalid credentials entered popup"""
        wrong_cred_msg = QMessageBox()
        wrong_cred_msg.setWindowTitle("Connection Failed")
        wrong_cred_msg.setText("Invalid Credentials!!! ")
        wrong_cred_msg.setIcon(QMessageBox.Critical)
        x = wrong_cred_msg.exec_()

    def test_success_popup(self):
        """Connection test successful popup"""
        success_msg = QMessageBox()
        success_msg.setWindowTitle("Connected to MySQL Database")
        success_msg.setText("Test Successful!!! ")
        success_msg.setIcon(QMessageBox.Information)
        success_msg.buttonClicked.connect(self.login_enable)

        x = success_msg.exec_()

    def login_enable(self, text):
        """Enables the login button once the test connection is successful"""
        self.mysql_login_page.login_pushButton.setEnabled(True)


    def access_db_page(self):
        """Access the db page"""
        self.db_window.show()
        self.db_page_initial_load()
        self.mysql_window.hide()

    def db_page_initial_load(self):
        """Disable buttons  when DB Page loads"""
        self.db_page.next_pushButton.setEnabled(False)
        self.db_page.reset_db_pushButton.setEnabled(False)

    def reset_fields(self):
        """Reset all the fields in the window"""
        self.mysql_login_page.uname_lineEdit.clear()
        self.mysql_login_page.paswd_lineEdit.clear()
        self.mysql_login_page.hname_lineEdit.clear()
        self.mysql_login_page.port_lineEdit.clear()
        self.mysql_login_page.paswd_lineEdit.setEnabled(False)
        self.mysql_login_page.hname_lineEdit.setEnabled(False)
        self.mysql_login_page.port_lineEdit.setEnabled(False)

    ### DB Page

    def handle_back_db_window(self):
        """Back button leads us to MySQL Window"""
        self.mysql_window.show()
        self.db_window.hide()

    def show_databases(self):
        """Shows the available databases"""
        try:
            print("Please wait, connecting to db...")
            con_obj=MySqlDatabase.create_db_connection()
            #print("CON OBJ IS", con_obj)
            sql_show_db = 'SHOW DATABASES'
            cur_show_db = con_obj.cursor()
            cur_show_db.execute(sql_show_db)

            l=[]
            for dbs in cur_show_db:
                for db in dbs:
                    #print(db)
                    l.append(db)
            #print("List of dbs:", l)
            db_list_linewise = "\n".join(l)

            self.db_page.show_db_textBrowser.setText(db_list_linewise)

            self.activate_db_combo(l)

        except Exception as e:

            print(e)

        finally:
            cur_show_db.close()
            con_obj.close()

    def activate_db_combo(self, db_list_linewise):
        """Combo box to be activated with list of dbs"""
        self.db_page.db_list_comboBox.addItem('None')
        index = self.db_page.db_list_comboBox.findText('None', QtCore.Qt.MatchFixedString)
        self.db_page.db_list_comboBox.setCurrentIndex(index)
        for l in db_list_linewise:
            self.db_page.db_list_comboBox.addItem(l)

        self.activate_db_reset()
        # self.next_pushButton.setEnabled(True)

    def activate_db_reset(self):
        """Activate the reset button in db page"""
        self.db_page.reset_db_pushButton.setEnabled(True)

    def reset_db_page_fields(self):
        """To reset all the fields in the db page"""
        self.db_page.show_db_textBrowser.clear()
        self.db_page.db_list_comboBox.clear()
        self.db_page.next_pushButton.setEnabled(False)


    def activate_next_db_window(self):
        """Activate next button which would lead to Table page"""
        self.db_page.next_pushButton.setEnabled(True)

    def access_table_page(self):
        """Access table page when Next button is clicked from the DB page"""
        self.table_window.show()
        self.table_page_initial_load()
        self.db_window.hide()

    def handle_back_table_window(self):
        """Back button in Table Page should lead us to the DB page"""
        self.db_window.show()
        self.table_window.hide()
        self.table_page.table_list_comboBox.clear()


    def table_page_initial_load(self):
        """Disable buttons  when Table Page loads"""
        self.table_page.reset_in_table_pushButton.setEnabled(False)
        self.table_page.next_in_tablepage_pushButton.setEnabled(False)

    ### Table Page

    def connect_to_db(self):
        """Establish connection with the selected db"""
        try:
            # user_input = self.get_credentials_from_user()[0]
            # password_input = self.get_credentials_from_user()[1]
            # host_input = self.get_credentials_from_user()[2]
            # port_input = self.get_credentials_from_user()[3]
            database_input = self.db_page.db_list_comboBox.currentText()
            print(database_input)
            #con_obj_for_table=mysql.connector.connect(user,password,host,database,port)
            con_obj_for_table = mysql.connector.connect(user = 'root' , password = 'pihul' , host = 'localhost' , port = str(3306), database=self.db_page.db_list_comboBox.currentText())

            # con_obj_for_table = mysql.connector.connect(user = self.get_credentials_from_user()[0],
            #                                             password = self.get_credentials_from_user()[1],
            #                                             host = self.get_credentials_from_user()[2],
            #                                             port = self.get_credentials_from_user()[3],
            #                                             database=self.db_page.db_list_comboBox.currentText())
            #print("hello")

            if con_obj_for_table.is_connected():
                print("Connection established with the database successfully")

        except Exception as e:
            print("Unable to establish connection with the database",e)

        return con_obj_for_table






    def show_tables(self):
        """Show available tables in the selected database"""
        sql_show_tables='SHOW TABLES'
        try:
            con_obj=self.connect_to_db()
            cur_show_tables=con_obj.cursor()
            cur_show_tables.execute(sql_show_tables)

            l = []
            for tables in cur_show_tables:
                for table in tables:
                    # print(db)
                    l.append(table)
            # print("List of dbs:", l)
            table_list_linewise = "\n".join(l)
            print(l)

            self.table_page.show_in_table_textBrowser.setText(table_list_linewise)

            self.activate_table_combo(l)

        except Exception as e:

            print(e)


        finally:
            cur_show_tables.close()
            con_obj.close()

    def activate_table_combo(self, table_list_linewise):
        """Combo box to be activated with list of tables"""
        self.table_page.table_list_comboBox.addItem('None')
        index = self.table_page.table_list_comboBox.findText('None', QtCore.Qt.MatchFixedString)
        self.table_page.table_list_comboBox.setCurrentIndex(index)
        for l in table_list_linewise:
            self.table_page.table_list_comboBox.addItem(l)

        self.activate_table_reset()
        # self.next_pushButton.setEnabled(True)

    def activate_table_reset(self):
        """Activate the reset button in table page"""
        self.table_page.reset_in_table_pushButton.setEnabled(True)


    def reset_table_page_fields(self):
        """Reset all the fields in the Table page"""
        self.table_page.show_in_table_textBrowser.clear()
        self.table_page.table_list_comboBox.clear()
        self.table_page.next_in_tablepage_pushButton.setEnabled(False)


    def activate_next_table_window(self):
        """Activate next button which would lead to Table info page"""
        self.table_page.next_in_tablepage_pushButton.setEnabled(True)


    def access_table_info_page(self):
        """Access table info page when Next button is clicked from the Table page"""

        try:
            self.table_info_window.show()
            self.table_info_page_initial_load()
            self.table_window.hide()
        except Exception as e:
            print(e)

    def table_info_page_initial_load(self):
        """Disable buttons  when Table Page loads"""
        self.table_info_page.reset_in_table_info_pushButton.setEnabled(False)
        self.table_info_page.next_in_table_info_pushButton.setEnabled(False)
        self.table_info_page.desc_table_in_table_info_pushButton.setEnabled(False)
        self.table_info_page.filter_cond_in_table_info_pushButton.setEnabled(False)
        self.table_info_page.show_tname_in_table_info_label.setEnabled(False)
        self.table_info_page.show_count_in_table_info_label.setEnabled(False)



    ### Table Page

    def handle_back_table_info_window(self):
        """Back button in Table Info Page should lead us to the Table page"""
        self.table_window.show()
        self.table_info_window.hide()

    def activate_tname_count_labels(self):
        """Activates the table name & count labels"""
        self.table_info_page.show_tname_in_table_info_label.setEnabled(True)
        self.table_info_page.show_count_in_table_info_label.setEnabled(True)

    def show_record_count(self):
        """Show record count for the selected table"""
        """Show record count from the selected table"""
        self.activate_tname_count_labels()
        table_input=self.table_page.table_list_comboBox.currentText()
        sql_show_cnt="SELECT * FROM " + '`' + table_input + '`'
        #print(sql_show_cnt)
        try:
            con_obj = self.connect_to_db()
            cur_show_rec_cnt = con_obj.cursor()
            cur_show_rec_cnt.execute(sql_show_cnt)
            cur_show_rec_cnt.fetchall()
            rc = cur_show_rec_cnt.rowcount
            print(cur_show_rec_cnt)
            #print(f"Record count for {table_input}=",rc)
            self.print_table_name_and_count(table_input,rc)
            self.activate_desc_table()

        except Exception as e:
            print('Unable to fetch record count....', e)
        finally:
            cur_show_rec_cnt.close()
            cur_show_rec_cnt.close()

    def print_table_name_and_count(self,tname,rc):
        """Prints the table name in the reqd label"""
        self.table_info_page.show_tname_in_table_info_label.setText(tname)
        self.table_info_page.show_count_in_table_info_label.setText(str(rc))

    def activate_desc_table(self):
        """Activates DESC Table push button"""
        self.table_info_page.desc_table_in_table_info_pushButton.setEnabled(True)


    def get_row_count(self):
        """"Gets the row count of DESC table, i.e., no. of columns in a table"""
        table_input = self.table_page.table_list_comboBox.currentText()
        sql_row_cnt = 'DESC ' + table_input
        try:
            con_obj = self.connect_to_db()
            cur_row_cnt = con_obj.cursor()
            cur_row_cnt.execute(sql_row_cnt)
            cur_row_cnt.fetchall()
            rc = cur_row_cnt.rowcount
            return rc
        except Exception as e:
            print(f"Couldn't fetch the no. of columns in the table {table_input}",e)

        finally:
            cur_row_cnt.close()
            con_obj.close()


    def desc_table(self):
        """Show the table description as in DESC <table name>"""
        col_headers=['Field','Type','Null','Key','Default','Extra']
        col_count=len(col_headers)
        row_count=self.get_row_count()
        print(row_count)
        self.table_info_page.se



















if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    my_window = QtWidgets.QMainWindow()
    main_obj = MySqlDatabase(my_window)
    main_obj.display_mysql_window()
    sys.exit(app.exec_())
