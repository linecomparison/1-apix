import os
import ftplib
import socket
import time
import logging
 
server     = 'appex.cl'
username   = 'apix@appex.cl'
password   = 'cy8h(V*+eF4T'
local_dir  = "D:/dev/funerariapp/apix/src/api"
remote_dir = "/src/api"

fmt = '%(asctime)s | %(levelname)s | %(message)s'
logging.basicConfig(level=logging.DEBUG, 
                    format=fmt, 
                    handlers=[logging.StreamHandler(), 
                              logging.FileHandler("ftp.log")])
while True:
    # First try/except block
    try:
        file_list = os.listdir(local_dir)

        # Validating if there are files
        if not file_list:
            logging.info("No files to upload, waiting for new files...")
            time.sleep(600)
            continue

        with ftplib.FTP_TLS(server, username, password) as ftp:
            ftp.prot_p()
            logging.info("Connection established with FTP server")

            ftp.cwd(remote_dir)
            logging.info(f"Accessing {remote_dir}")

            for file_name in file_list:
                # Second try/except block
                try:
                    file_path = os.path.join(local_dir, file_name)
                    if os.path.isfile(file_path):
                        with open(file_path, 'rb') as file:
                            logging.info(f"Uploading {file_name}...")
                            ftp.storbinary(f'STOR {file_name}', file)
                        os.remove(file_path)
                except Exception as e:
                    logging.error(f'Error uploading {file_name}: {str(e)}')
                    continue

            logging.info(f"Uploaded all files to {remote_dir}")

        logging.info(f"The process will restart in two hours")
        time.sleep(7200)

    except socket.gaierror:
        logging.critical('Invalid Hostname.')
        break

    except ftplib.error_perm:
        logging.critical('Invalid username, password or remote '
                         'directory path.')
        break

    except FileNotFoundError:
        logging.critical(f'{local_dir} is not a valid directory.' 
                          'Please check path informed.')
        break
