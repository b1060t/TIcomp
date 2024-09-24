import os
import glob

# Parse files in the raw directory
pattern = 'data/raw/*/*'
dcmlist = list(glob.glob(f'{pattern}'))
for directory in dcmlist:
    files = os.listdir(directory)
    for file in files:
        if file.startswith('.'):
            os.remove(os.path.join(directory, file))
dcmlist = [x.replace('-', '_') for x in dcmlist]
dcmlist = [x[9:] for x in dcmlist]
print(dcmlist)
pathlist = dcmlist
dcmlist = [str.split(d, '/')[1] for d in dcmlist]
dcmlist = [
    str.split(d, '_') for d in dcmlist
]
dcmlist = [[pathlist[i]] + dcmlist[i] for i in range(len(dcmlist))]
cohort = {}
for rec in dcmlist:
    print(rec)
    if len(rec) > 2:
        path = rec[0]
        last_name = rec[1]
        first_name = rec[2]
        cat = rec[3][:4]
        subj = rec[3][4:]
        id = rec[3]
        ses = rec[4]
    else:
        continue
        
    if id in cohort.keys():
        cohort[id]['raw_dir'].update({ses: path})
    else:
        cohort[id] = {
            'name': f'{last_name}_{first_name}',
            'group': cat,
            'subj': subj,
            'id': id,
            'raw_dir': {}
        }
        cohort[id]['raw_dir'].update({ses: path})
raw_root = os.path.join(os.getcwd(), 'data', 'raw')
nii_root = os.path.join(os.getcwd(), 'data', 'nii')
def dcm2nii(src, dst, filename):
    cmd = 'dcm2niix -z y -f {} -w 0 -o {} {}'.format(filename, dst, src)
    os.system(cmd)
def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.mkdir(path)
def extract_path(rec):
    print(rec)
    path_anat = os.listdir(os.path.join(raw_root, rec['raw_dir']['ANAT']))
    path_11 = os.listdir(os.path.join(raw_root, rec['raw_dir']['11']))
    path_51 = os.listdir(os.path.join(raw_root, rec['raw_dir']['51']))
    path_52 = os.listdir(os.path.join(raw_root, rec['raw_dir']['52']))
    if '4week' in rec['raw_dir'].keys():
        path_4week = os.listdir(os.path.join(raw_root, rec['raw_dir']['4week']))
    path_t1 = [p for p in path_anat if 't1' in p][0]
    path_t1 = os.path.join(raw_root, rec['raw_dir']['ANAT'], path_t1)
    path_bold_10 = [p for p in path_anat if 'bold' in p][0]
    path_bold_10 = os.path.join(raw_root, rec['raw_dir']['ANAT'], path_bold_10)
    path_dti_dir64 = [p for p in path_anat if 'dir64' in p][0]
    path_dti_dir64 = os.path.join(raw_root, rec['raw_dir']['ANAT'], path_dti_dir64)
    path_dti_b0 = [p for p in path_anat if 'b0' in p][0]
    path_dti_b0 = os.path.join(raw_root, rec['raw_dir']['ANAT'], path_dti_b0)
    path_bold_111 = [p for p in path_11 if 'bold' in p][0]
    path_bold_111 = os.path.join(raw_root, rec['raw_dir']['11'], path_bold_111)
    path_bold_112 = [p for p in path_11 if 'bold' in p][1]
    path_bold_112 = os.path.join(raw_root, rec['raw_dir']['11'], path_bold_112)
    path_bold_511 = [p for p in path_51 if 'bold' in p][0]
    path_bold_511 = os.path.join(raw_root, rec['raw_dir']['51'], path_bold_511)
    path_bold_512 = [p for p in path_51 if 'bold' in p][1]
    path_bold_512 = os.path.join(raw_root, rec['raw_dir']['51'], path_bold_512)
    path_bold_52 = [p for p in path_52 if 'bold' in p][0]
    path_bold_52 = os.path.join(raw_root, rec['raw_dir']['52'], path_bold_52)
    if '4week' in rec['raw_dir'].keys():
        path_bold_4week = [p for p in path_4week if 'bold' in p][0]
        path_bold_4week = os.path.join(raw_root, rec['raw_dir']['4week'], path_bold_4week)
    id = rec['id']
    subj_root = os.path.join(nii_root, 'sub-'+id)
    mkdir_if_not_exist(subj_root)
    ses_anat_root = os.path.join(subj_root, 'ses-0')
    mkdir_if_not_exist(ses_anat_root)
    ses_11_root = os.path.join(subj_root, 'ses-11')
    mkdir_if_not_exist(ses_11_root)
    ses_51_root = os.path.join(subj_root, 'ses-51')
    mkdir_if_not_exist(ses_51_root)
    ses_52_root = os.path.join(subj_root, 'ses-52')
    mkdir_if_not_exist(ses_52_root)
    if '4week' in rec['raw_dir'].keys():
        ses_6_root = os.path.join(subj_root, 'ses-6')
        mkdir_if_not_exist(ses_6_root)
    tmp_root = os.path.join(ses_anat_root, 'anat')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-0_T1w'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_t1, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_anat_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-0_task-rest_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_10, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_anat_root, 'dwi')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-0_dwi_dir64'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_dti_dir64, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_anat_root, 'dwi')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-0_dwi_b0'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_dti_b0, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_11_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-11_task-rest_run-01_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_111, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_11_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-11_task-rest_run-02_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_112, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_51_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-51_task-rest_run-01_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_511, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_51_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-51_task-rest_run-02_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_512, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    tmp_root = os.path.join(ses_52_root, 'func')
    mkdir_if_not_exist(tmp_root)
    file_name = 'sub-{}_ses-52_task-rest_bold'.format(id)
    if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
        dcm2nii(path_bold_52, tmp_root, file_name)
    else:
        print('File exists: {}'.format(file_name))
    if '4week' in rec['raw_dir'].keys():
        tmp_root = os.path.join(ses_6_root, 'func')
        mkdir_if_not_exist(tmp_root)
        file_name = 'sub-{}_ses-6_task-rest_bold'.format(id)
        if not os.path.exists(os.path.join(tmp_root, file_name + '.nii.gz')):
            dcm2nii(path_bold_4week, tmp_root, file_name)
        else:
            print('File exists: {}'.format(file_name))
    del rec['raw_dir']
    return rec
cohort = [extract_path(rec) for rec in cohort.values()]

# Parse records