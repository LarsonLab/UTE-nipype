__author__ = 'usuresh'

from nipype.interfaces.base import (BaseInterface, TraitedSpec, traits, File,
                                    OutputMultiPath, BaseInterfaceInputSpec,
                                    isdefined, InputMultiPath)

from ...config import config
from glob import glob
import os
from ...base import register_workflow, PBRBaseInputSpec, PBRBaseInterface

class UteInputSpec(PBRBaseInputSpec):
    foo = InputMultiPath(File(exists=True))

class UteOutputSpec(TraitedSpec):
    pass
    # for now, nothing is output, but later there will be outputs

class Ute(PBRBaseInterface):
    input_spec = UteInputSpec
    output_spec = UteOutputSpec #fix
    #stuff AK added to the Nipype stuff
    flag = "ute" #this is for pbr mse# -w interfacename
    connections = [("nifti", "t1_files", "foo")]
    # auto-assemble connections: take the nifti interface's output called "t1_files" 
    # and connect to the this interfaces input called "foo"

    def _run_interface_pbr(self, runtime):
      #insert workflow here:
      import nipype.interfaces.fsl as fsl
      import nipype.pipeline.engine as pe
      import nipype.interfaces.freesurfer as fs
      import nipype.interfaces.io as nio
      
      bet = pe.MapNode(interface=fsl.BET(), name = 'bet', iterfield=['frac'])
      bet.inputs.in_file = #define in_file right here
      bet.inputs.frac = [0.7, 0.5, 0.3]
      
      fast = pe.MapNode(interface=fsl.FAST(), name='fast', iterfield=['in_files'])
      ss = pe.MapNode(interface=fs.SegStats(), name='ss', iterfield=['segmentation_file'])
      
      ds = pe.Node(interface=nio.DataSink(), name="ds", iterfield=['in_files'])
      ds.inputs.base_directory = #define the output here 
      
      workflow = pe.Workflow(name='ute_flow')
      workflow.base_dir = '.'
      
      workflow.connect([(bet, fast, [('out_file', 'in_files')]), (fast, ss,[('mixeltype', 'segmentation_file')]), (ss, ds, [('avgwf_file', 'in_files')])]) 
      
      workflow.run()

      """print(self.inputs)""" 
      #this was used for checking if the workflow was being triggered and run
      #vi inserted into ucsf server side ute.py
      return runtime 


    def _get_output_folder(self):
        return "ute"

    def _list_outputs(self):
        outputs = self._outputs().get()
        #we don't have any outputs yet, but when you do, you
        # need to define how to find them
        #outputs["bar"] = glob()  

        return outputs

register_workflow(Ute)
# always remeber to use 'python setup.py install' after every change iteration
