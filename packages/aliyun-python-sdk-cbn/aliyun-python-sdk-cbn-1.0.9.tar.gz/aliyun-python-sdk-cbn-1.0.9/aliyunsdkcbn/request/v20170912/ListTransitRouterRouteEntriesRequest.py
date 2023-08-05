# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkcbn.endpoint import endpoint_data

class ListTransitRouterRouteEntriesRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'Cbn', '2017-09-12', 'ListTransitRouterRouteEntries','cbn')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_ResourceOwnerId(self):
		return self.get_query_params().get('ResourceOwnerId')

	def set_ResourceOwnerId(self,ResourceOwnerId):
		self.add_query_param('ResourceOwnerId',ResourceOwnerId)

	def get_TransitRouterRouteEntryDestinationCidrBlock(self):
		return self.get_query_params().get('TransitRouterRouteEntryDestinationCidrBlock')

	def set_TransitRouterRouteEntryDestinationCidrBlock(self,TransitRouterRouteEntryDestinationCidrBlock):
		self.add_query_param('TransitRouterRouteEntryDestinationCidrBlock',TransitRouterRouteEntryDestinationCidrBlock)

	def get_TransitRouterRouteTableId(self):
		return self.get_query_params().get('TransitRouterRouteTableId')

	def set_TransitRouterRouteTableId(self,TransitRouterRouteTableId):
		self.add_query_param('TransitRouterRouteTableId',TransitRouterRouteTableId)

	def get_NextToken(self):
		return self.get_query_params().get('NextToken')

	def set_NextToken(self,NextToken):
		self.add_query_param('NextToken',NextToken)

	def get_TransitRouterRouteEntryStatus(self):
		return self.get_query_params().get('TransitRouterRouteEntryStatus')

	def set_TransitRouterRouteEntryStatus(self,TransitRouterRouteEntryStatus):
		self.add_query_param('TransitRouterRouteEntryStatus',TransitRouterRouteEntryStatus)

	def get_ResourceOwnerAccount(self):
		return self.get_query_params().get('ResourceOwnerAccount')

	def set_ResourceOwnerAccount(self,ResourceOwnerAccount):
		self.add_query_param('ResourceOwnerAccount',ResourceOwnerAccount)

	def get_OwnerAccount(self):
		return self.get_query_params().get('OwnerAccount')

	def set_OwnerAccount(self,OwnerAccount):
		self.add_query_param('OwnerAccount',OwnerAccount)

	def get_TransitRouterRouteEntryNamess(self):
		return self.get_query_params().get('TransitRouterRouteEntryNames')

	def set_TransitRouterRouteEntryNamess(self, TransitRouterRouteEntryNamess):
		for depth1 in range(len(TransitRouterRouteEntryNamess)):
			if TransitRouterRouteEntryNamess[depth1] is not None:
				self.add_query_param('TransitRouterRouteEntryNames.' + str(depth1 + 1) , TransitRouterRouteEntryNamess[depth1])

	def get_TransitRouterRouteEntryIdss(self):
		return self.get_query_params().get('TransitRouterRouteEntryIds')

	def set_TransitRouterRouteEntryIdss(self, TransitRouterRouteEntryIdss):
		for depth1 in range(len(TransitRouterRouteEntryIdss)):
			if TransitRouterRouteEntryIdss[depth1] is not None:
				self.add_query_param('TransitRouterRouteEntryIds.' + str(depth1 + 1) , TransitRouterRouteEntryIdss[depth1])

	def get_OwnerId(self):
		return self.get_query_params().get('OwnerId')

	def set_OwnerId(self,OwnerId):
		self.add_query_param('OwnerId',OwnerId)

	def get_MaxResults(self):
		return self.get_query_params().get('MaxResults')

	def set_MaxResults(self,MaxResults):
		self.add_query_param('MaxResults',MaxResults)