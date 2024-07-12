import { useDomainName } from '@/hooks';
import { uploadTurtleFileBrickapiV1DomainsDomainUploadPost } from '@/services/brick-server-playground/domains';
import { PageContainer, ProCard, ProForm, ProFormUploadButton } from '@ant-design/pro-components';
import { message } from 'antd';
const Settings: React.FC = () => {
  const domainName = useDomainName();
  const onFinishUploadFile = async (values: { file: any }) => {
    if (!values.file || values.file.length !== 1) {
      message.error(`Error: no file selected!`);
      return;
    }
    const result = await uploadTurtleFileBrickapiV1DomainsDomainUploadPost(
      { domain: domainName },
      {},
      values.file[0].originFileObj,
    );
    if (result.errorCode !== 'Success') {
      message.error(`Error: ${result.errorCode}`);
    } else {
      message.success(`File uploaded!`);
    }
  };
  return (
    <PageContainer>
      <ProCard title="Upload Turtle File">
        <ProForm onFinish={onFinishUploadFile}>
          <ProFormUploadButton
            title="Select a file"
            name="file"
            max={1}
            accept=".ttl"
            rules={[
              {
                required: true,
                message: 'Please choose a file.',
              },
            ]}
          />
        </ProForm>
      </ProCard>
    </PageContainer>
  );
};

export default Settings;
