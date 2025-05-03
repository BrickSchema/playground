import { useDomainName } from '@/hooks';
import {
  deleteResourceBrickapiV1DomainsDomainResourcesDelete,
  listResourcesBrickapiV1DomainsDomainResourcesGet,
  updateResourceBrickapiV1DomainsDomainResourcesPost,
} from '@/services/brick-server-playground/domains';
import { PlusOutlined } from '@ant-design/icons';
import {
  ActionType,
  ModalForm,
  PageContainer,
  ProColumns,
  ProFormGroup,
  ProFormText,
  ProTable,
} from '@ant-design/pro-components';
import { Button, Popconfirm, message } from 'antd';
import React, { useRef, useState } from 'react';

const ResourceList: React.FC = () => {
  const domainName = useDomainName();
  const actionRef = useRef<ActionType>();
  const [isAddResourceOpen, setIsAddResourceOpen] = useState<boolean>(false);
  const [currentResource, setCurrentResource] = useState<API.ResourceConstraintRead | undefined>(
    undefined,
  );

  const onClickAddResource = async () => {
    setCurrentResource(undefined);
    setIsAddResourceOpen(true);
  };

  const onClickEditResource =  async(resource: API.ResourceConstraintRead) => {
    setCurrentResource(resource);
    setIsAddResourceOpen(true);
  }

  const onFinishAddResource = async (values: { entityId: string; value: number }) => {
    console.log(values);
    const result = await updateResourceBrickapiV1DomainsDomainResourcesPost(
      { domain: domainName },
      { entityId: values.entityId, value: values.value },
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    await actionRef.current?.reload();
    setCurrentResource(undefined);
    setIsAddResourceOpen(false);
  };

  const onCancelAddResource = async () => {
    setIsAddResourceOpen(false);
  };

  const onDeleteResource = async (resource: API.ResourceConstraintRead) => {
    const result = await deleteResourceBrickapiV1DomainsDomainResourcesDelete({
      domain: domainName,
    }, {entityId: resource.entityId,});
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    await actionRef.current?.reload();
  };

  const columns: ProColumns<API.ResourceConstraintRead>[] = [
    {
      title: 'Entity',
      dataIndex: 'entityId',
    },
    {
      title: 'Value',
      dataIndex: 'value',
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="add_profile" onClick={() => onClickEditResource(record)}>
          Edit
        </a>,
        <Popconfirm
          key="delete"
          title="Delete the Resource Constraint"
          description="Are you sure to delete this resource constraint?"
          onConfirm={async () => onDeleteResource(record)}
        >
          <a>Delete</a>
        </Popconfirm>,
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable<API.ResourceConstraintRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        request={async (params, sort, filter) => {
          const result = await listResourcesBrickapiV1DomainsDomainResourcesGet({
            domain: domainName,
          });
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={onClickAddResource}>
            Add Resource Constraint
          </Button>,
        ]}
      />
      <ModalForm
        title={'Add Resource Constraint to Domain'}
        open={isAddResourceOpen}
        onFinish={onFinishAddResource}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelAddResource,
        }}
      >
        <ProFormGroup>
          <ProFormText
            label="Entity"
            name="entityId"
            width="md"
            initialValue={currentResource?.entityId || ""}
            rules={[
              {
                required: true,
                message: 'Please enter entity id.',
              },
            ]}
          />
          <ProFormText
            label="Value"
            name="value"
            width="md"
            initialValue={currentResource?.value || ""}
            rules={[
              {
                required: true,
                message: 'Please enter value.',
              },
            ]}
          />
        </ProFormGroup>
      </ModalForm>
    </PageContainer>
  );
};

export default ResourceList;
