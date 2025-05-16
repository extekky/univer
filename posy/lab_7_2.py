import sys
from ftplib import FTP


def download_file(server, username, password, remote_path):
    local_filename = 'ftp_out'

    ftp = FTP(server)
    ftp.set_debuglevel(0)
    ftp.login(user=username, passwd=password)
    ftp.sendcmd('PASV')  # Переходим в пассивный режим

    with open(local_filename, 'wb') as local_file:
        def callback(data):
            local_file.write(data)

        # Выполняем команду
        ftp.retrbinary(f'RETR {remote_path}', callback)

    ftp.quit()


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Что то не так :(")
        sys.exit(1)

    server = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    remote_path = sys.argv[4]

    download_file(server, username, password, remote_path)
