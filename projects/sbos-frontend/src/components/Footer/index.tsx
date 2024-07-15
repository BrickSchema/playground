import { GithubOutlined } from '@ant-design/icons';
import { GlobalFooter } from '@ant-design/pro-layout/es/components/GlobalFooter';
import React from 'react';

const Footer: React.FC = () => {
  return (
    <GlobalFooter
      style={{
        background: 'none',
        marginTop: '12px',
        marginBottom: '12px',
      }}
      copyright={false}
      links={[
        // {
        //   key: 'brick',
        //   title: 'Brick',
        //   href: 'https://brickschema.org/',
        //   blankTarget: true,
        // },
        {
          key: 'github',
          title: <GithubOutlined />,
          href: 'https://github.com/BrickSchema/brick-example-server',
          blankTarget: true,
        },
        // {
        //   key: 'Ant Design',
        //   title: 'Ant Design',
        //   href: 'https://ant.design',
        //   blankTarget: true,
        // },
      ]}
    />
  );
};

export default Footer;
