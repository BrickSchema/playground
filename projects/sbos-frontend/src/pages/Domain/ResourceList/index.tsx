import { useDomainName } from '@/hooks';
import {
  deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDelete,
  listResourcesBrickapiV1DomainsDomainResourcesGet,
  updateResourceBrickapiV1DomainsDomainResourcesEntityIdPost,
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

  const onClickAddResource = async () => {
    setIsAddResourceOpen(true);
  };

  const onFinishAddResource = async (values: { entityId: string; value: number }) => {
    console.log(values);
    const result = await updateResourceBrickapiV1DomainsDomainResourcesEntityIdPost(
      { domain: domainName, entity_id: values.entityId },
      { value: values.value },
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    await actionRef.current?.reload();
    setIsAddResourceOpen(false);
  };

  const onCancelAddResource = async () => {
    setIsAddResourceOpen(false);
  };

  const onDeleteResource = async (resource: API.ResourceConstraintRead) => {
    const result = await deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDelete({
      domain: domainName,
      entity_id: resource.entityId,
    });
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
        // <a key="add_profile" onClick={() => onClickAddProfile(record)}>Add Profile</a>,
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
