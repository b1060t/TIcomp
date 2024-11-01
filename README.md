# TI
## Session Annotations
1. Session 0: Pre-stimulation MRI
    T1w
    DTI
    rs-fMRI
2. Session 11: Concurrent TI-fMRI (first session)
    rs-fMRI * 2
3. Session 51: Concurrent TI-fMRI (final session)
    rs-fMRI * 2
4. Session 52: Post-stimulation MRI
    rs-fMRI
5. Session 6: Follow-up MRI
    rs-fMRI

## fMRIPrep commands
```bash
fmriprep-docker nii fmriprep -i nipreps/fmriprep:latest --fs-license-file ~/freesurfer/license.txt -w ../tmp --fs-no-reconall --output-spaces MNI152NLin2009cAsym 
```