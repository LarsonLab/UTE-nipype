import nipype.interfaces.fsl as fsl
import nipype.pipeline.engine as pe
import nipype.interfaces.freesurfer as fs
import nipype.interfaces.io as nio


bet = pe.MapNode(interface=fsl.BET(), name = 'bet', iterfield=['frac'])
bet.inputs.in_file = '/data/henry1/uday/ms1297-mse4664-007-MPRAGE_iso_1.nii.gz'
#use the absolute path instead of relative path here
bet.inputs.frac = [0.7, 0.5, 0.3]
#can now adjust to process through different fracs
#fast = pe.Node(interface=fsl.FAST(), name='fast')
fast = pe.MapNode(interface=fsl.FAST(), name='fast', iterfield=['in_files'])
ss = pe.MapNode(interface=fs.SegStats(), name='ss', iterfield=['segmentation_file'])
#iterate over a list of fast outputs as a mapnode, iterfield = in_files  

#setting up the DataSink for organizing outputs 
ds = pe.Node(interface=nio.DataSink(), name="ds", iterfield=['in_files'])
ds.inputs.base_directory = '/data/henry1/uday/ds_output'
#this is broken -- need to find a way to use DataSink as MapNode
#fixed, use base_directory rather than base.directory
#no object DataSink within this -- iterfield is broken too | use infields keyword arg 


workflow = pe.Workflow(name='MapNodeFlow')
workflow.base_dir = '.'

workflow.connect([(bet, fast, [('out_file', 'in_files')]), (fast, ss,[('mixeltype', 'segmentation_file')]), (ss, ds, [('avgwf_file', 'in_files')])]) 
#for FAST use mixeltypes instead of out_files 
#datasink works the same but you can invent the input and it'll create a file though 
#unsure about this third connection of ds to ss 
#no ss outfiles -- fixed by using avgwf_file

workflow.run() 
#check the JSONS for t1 files and know that eventually the UTE files will have another field called UTE 
#less status.JSON
#check nii/status.JSON


