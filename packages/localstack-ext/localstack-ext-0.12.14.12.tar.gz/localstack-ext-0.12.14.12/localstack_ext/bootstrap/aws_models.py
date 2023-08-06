from localstack.utils.aws import aws_models
BRJnE=super
BRJnu=None
BRJnF=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BRJnE(LambdaLayer,self).__init__(arn)
  self.cwd=BRJnu
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.BRJnF.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(RDSDatabase,self).__init__(BRJnF,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(RDSCluster,self).__init__(BRJnF,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(AppSyncAPI,self).__init__(BRJnF,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(AmplifyApp,self).__init__(BRJnF,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(ElastiCacheCluster,self).__init__(BRJnF,env=env)
class TransferServer(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(TransferServer,self).__init__(BRJnF,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(CloudFrontDistribution,self).__init__(BRJnF,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,BRJnF,env=BRJnu):
  BRJnE(CodeCommitRepository,self).__init__(BRJnF,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
