import {
  ActionType,
  ModalForm,
  PageContainer,
  ProColumns,
  ProFormGroup,
  ProFormText,
  ProTable
} from '@ant-design/pro-components';
import React, {useRef, useState} from 'react';
import {useDomainName} from "@/hooks";
import {
  createDomainBrickapiV1DomainsDomainPost,
  initDomainBrickapiV1DomainsDomainInitGet,
  listDomainsBrickapiV1DomainsGet,
} from "@/services/brick-server-playground/domains";
import {Button, message, Popconfirm} from "antd";
import {PlusOutlined} from "@ant-design/icons";

const DomainList: React.FC = () => {
  // const domainName = useDomainName();
  const actionRef = useRef<ActionType>();
  const [isAddDomainOpen, setIsAddDomainOpen] = useState<boolean>(false);
  const [currentDomain, setCurrentDomain] = useState<API.ResourceConstraintRead | undefined>(
    undefined,
  );

  const onClickAddResource = async () => {
    setCurrentDomain(undefined);
    setIsAddDomainOpen(true);
  };

  const onClickInitDomain =  async(domain: API.DomainRead) => {
    const result = await  initDomainBrickapiV1DomainsDomainInitGet({domain: domain.name});
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      message.success(`Domain ${domain.name} initialized!`);
    }
  }

  const onFinishAddDomain = async (values: { name: string; }) => {
    console.log(values);
    const result = await createDomainBrickapiV1DomainsDomainPost(
      { domain: values.name },
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    }
    await actionRef.current?.reload();
    setCurrentDomain(undefined);
    setIsAddDomainOpen(false);
  };

  const onCancelAddResource = async () => {
    setIsAddDomainOpen(false);
  };


  const columns: ProColumns<API.DomainRead>[] = [
    {
      title: 'Name',
      dataIndex: 'name',
    },
    {
      title: 'Operations',
      valueType: 'option',
      render: (text, record, _, action) => [
        <a key="add_profile" onClick={() => onClickInitDomain(record)}>
          Init
        </a>
      ],
    },
  ];

  return (
    <PageContainer>
      <ProTable<API.DomainRead>
        actionRef={actionRef}
        columns={columns}
        pagination={false}
        search={false}
        request={async (params, sort, filter) => {
          const result = await listDomainsBrickapiV1DomainsGet();
          return {
            data: result.data?.results || [],
            success: true,
            total: result.data?.count || 0,
          };
        }}
        toolBarRender={() => [
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={onClickAddResource}>
            Create Domain
          </Button>,
        ]}
      />
      <ModalForm
        title={'Create Domain'}
        open={isAddDomainOpen}
        onFinish={onFinishAddDomain}
        modalProps={{
          destroyOnClose: true,
          onCancel: onCancelAddResource,
        }}
      >
        <ProFormGroup>
          <ProFormText
            label="Name"
            name="name"
            width="md"
            rules={[
              {
                required: true,
                message: 'Please enter domain name.',
              },
            ]}
          />
        </ProFormGroup>
      </ModalForm>
    </PageContainer>
  );
};
export default DomainList;
