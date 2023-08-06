from localstack.utils.aws import aws_models
LVSWx=super
LVSWt=None
LVSWm=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  LVSWx(LambdaLayer,self).__init__(arn)
  self.cwd=LVSWt
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.LVSWm.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(RDSDatabase,self).__init__(LVSWm,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(RDSCluster,self).__init__(LVSWm,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(AppSyncAPI,self).__init__(LVSWm,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(AmplifyApp,self).__init__(LVSWm,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(ElastiCacheCluster,self).__init__(LVSWm,env=env)
class TransferServer(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(TransferServer,self).__init__(LVSWm,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(CloudFrontDistribution,self).__init__(LVSWm,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,LVSWm,env=LVSWt):
  LVSWx(CodeCommitRepository,self).__init__(LVSWm,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
