import os
import sys
import pathlib
import confg as cf

def move_file(src, dest):
    os.rename(src, dest)
    print(f'moved:: {src} >>> {dest}')

def get_all_folders(dir):
    return (dir, next(os.walk(dir))[1])

def get_all_files(dir):
    # RETURNS ALL FILES IN DIRECTORY AS OBJECT
    return list(pathlib.Path(dir).glob('**/*'))

def get_all_loose_files(dirs):
    # FOR ALL SOURCE DIRECTORIES, GET ALL FILES AND COMEBINE INTO SINGLE LIST
    loose_files = sum(list(map(lambda folder: get_all_files(folder), dirs)), [])
    return loose_files

def get_all_destination_folders(dirs):
    # FOR ALL DESTINATION DIRECTORIES, GET ALL FIRST LEVEL SUBDIRECTORY AND COMEBINE INTO SINGLE LIST
    # RETURNS TUPLE: (path, foldername, [foldername parts])
    pre_dest_folders = list(map(lambda folder: get_all_folders(folder), dirs))
    dest_folders = []

    for folder in pre_dest_folders:
        dest_folders.append(
            list(map(lambda fld: (
                folder[0],
                fld,
                fld.lower().split(' ')
            ), folder[1]))
        )

    dest_folders = sum(dest_folders, [])
    return dest_folders


def move_out_staging():
    source_folder_list = []
    destination_folder_list = []

    if os.path.exists(cf.STAGE_FOLDER):

        # CHECK IF FILES IN 'STAGING' FOLDER
        stage_files = get_all_loose_files([cf.STAGE_FOLDER])
        stage_files_ct = len(stage_files)
        if stage_files_ct > 0:
            input_str = f'There are {stage_files_ct} file{("s" if stage_files_ct > 0 else "")} in staging folder [{cf.STAGE_FOLDER}], move to destination folders (Y or N)?  '
            clean_stage = input(input_str).lower().strip()

            # ASK IF FILES IN STAGING SHOULD BE MOVED TO DESTINATION FOLDERS
            if (clean_stage not in ['y', 'n']):
                print('Invalid response, exiting')
                quit()
            elif (clean_stage == 'y'):
                source_folder_list = [cf.STAGE_FOLDER]
                destination_folder_list = cf.DESTINATION_FOLDER.split('|')

    return source_folder_list, destination_folder_list


def match_files(source_folder_list, destination_folder_list):
    found_files = []
    loose_files = get_all_loose_files(source_folder_list)

    dest_folders = get_all_destination_folders(destination_folder_list)
    ignore_dest_folders = cf.IGNORE_DESTINATION_FOLDER.lower().split(',')

    # ALL 'LOOSE' FILES
    for file in loose_files:

        file_name = file.name.lower()

        # CHECK ALL DESTINATION FOLDER IF A MATCH
        for folder in dest_folders:

            # SKIP FOLDER IF TO BE IGNORED
            if folder[1].lower() in ignore_dest_folders:
                continue

            # MATCH EACH WORD IN DESTINATION FOLDER TO FILENAME
            file_found = True
            for name in folder[2]:
                file_found = file_found and (name in file_name)

                # IF ANY PART OF DESTINATION FOLDER NAME NOT FOUND, SKIP FOLDER
                if not file_found:
                    break
        
            # IF ALL PARTS OF DESTINATION FOLDER NAME FOUND, ADD TO FOUND LIST AND MOVE TO NEXT FILE
            if file_found:
                found_files.append((
                    file,
                    folder
                ))
                break
    
    return found_files


if (__name__ == '__main__'):
    
    source_folder_list = []
    destination_folder_list = []

    # CHECK IF SOURCE PATH PASSED IN AS ARGUMENT
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        source_folder_list = [sys.argv[1]]
    elif len(sys.argv) > 1 and not os.path.exists(sys.argv[1]):
        print(f'Supplied path [{sys.argv[1]}] is not found, exiting')
        quit()
    else:
        # OFFER TO MOVE FILES FROM STAGING TO DESTINATION
        source_folder_list, destination_folder_list = move_out_staging()

    # IF FILES IN STAGING NOT MOVING TO DESTINATION
    # GET SOURCE FOLDERS FROM CONFIG FILE
    if len(source_folder_list) == 0:
        source_folder_list = cf.SOURCE_FOLDERS.split('|')

    if len(destination_folder_list) == 0:
        destination_folder_list = cf.DESTINATION_FOLDER.split('|')

    found_files = match_files(source_folder_list, destination_folder_list)

    for found in found_files:
        print(f'{str(found[0])} >>> {os.path.join(found[1][0], found[1][1])}')
    print()

    # ASK IF MATCHED FILES SHOULD BE MOVED?
    input_str = f'Move these files to destination (Y or N)? '
    move_it = input(input_str).lower()

    if (move_it not in ['y', 'n']):
        print('Invalid response, exiting')
        quit()
    elif (move_it == 'y'):
        for found in found_files:

            # IF NOT MOVING FROM STAGING FOLDER, MOVE MATCHED FILES TO STAGING FOLDER
            dest_dir = os.path.join(found[1][0], found[1][1])
            if source_folder_list[0] != cf.STAGE_FOLDER:
                dest_dir = cf.STAGE_FOLDER

            move_file(str(found[0]), os.path.join(dest_dir, found[0].name))

        print()

        if source_folder_list[0] != cf.STAGE_FOLDER:
            print(f'Files have been moved to staging folder [{cf.STAGE_FOLDER}].')
            print(f'Please run this again to move files from staging to destination - this is so files can be reviewed before final move.')
