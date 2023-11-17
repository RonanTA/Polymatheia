def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    from pysftp import Connection, CnOpts
    import os
    import json
    import datetime
    from io import BytesIO
    from google.cloud import storage
    
    todayDate = datetime.datetime.today()
    yesterdayDate = todayDate - datetime.timedelta(days = 1)
    yesterdayAtNoon = yesterdayDate.replace(hour=12, minute=0, second=0, microsecond=0)
    year = todayDate.year
    year2 = f'{todayDate.year}'[-2]+f'{todayDate.year}'[-1]
    month = f'{todayDate.month:02d}'
    today = f'{todayDate.day:02d}'
    yesterday = f'{yesterdayDate.day:02d}'

    sub_path = f'Archive/{year}/{month}'

    secret_location = '/secrets/ftp'

    with open(secret_location) as f:
        sftp_secrets = json.load(f)
        f.close()

    print("Creating FTP connection")
    cnopts = CnOpts()
    cnopts.hostkeys = None
    with Connection(sftp_secrets["host"], username=sftp_secrets["user"], password=sftp_secrets["pwd"], cnopts=cnopts) as sftp:
        print("Logged in")

        if (not sftp.isdir("OctaveVersAdeo")):
            raise Exception('ERROR: Folder OctaveVersAdeo does not exists.')

        with sftp.cd("OctaveVersAdeo"):
            folders = sftp.listdir()

            octave_folders = list(filter(lambda d: d.startswith("OCT"), folders))
            print(octave_folders)
            for folder in octave_folders:
                current_folder_to_search = f'{folder}/{sub_path}'
                today_files = list(filter(lambda fil: f'{year2}{month}{today}' in fil , sftp.listdir(current_folder_to_search)))
                yesterday_files = list(filter(lambda fil: f'{year2}{month}{yesterday}' in fil and datetime.datetime.fromtimestamp(sftp.stat(f'{current_folder_to_search}/{fil}').st_mtime) > yesterdayAtNoon , sftp.listdir(current_folder_to_search)))
                files_to_download = today_files + yesterday_files
                print(f'files to download : {files_to_download}')
                for file_to_download in files_to_download:
                    storage_client = storage.Client()
                    bucket = storage_client.bucket("prod-dataflow-bucket-etl")
                    filename = os.path.basename(file_to_download)
                    blob = bucket.blob(f'data/{filename}', chunk_size=2097152)
                    print(f'downloading file : "{file_to_download}"')
                    with sftp.open(f'{current_folder_to_search}/{file_to_download}', bufsize=1280000) as f:
                        blob.upload_from_file(f)

        sftp.close()
    return 'Sucess!'