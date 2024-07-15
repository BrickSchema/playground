import {
  getDomainBrickapiV1DomainsDomainGet,
  getDomainUserBrickapiV1DomainsDomainUsersUserGet,
} from '@/services/brick-server-playground/domains';
import { useEffect } from 'react';
import { useModel, useParams } from 'umi';

export const useDomainName = () => {
  const { initialState, setInitialState } = useModel('@@initialState');
  let { domainName } = useParams<{ domainName: string }>();
  domainName = domainName || '';
  useEffect(() => {
    const setDomain = async () => {
      const domain = await getDomainBrickapiV1DomainsDomainGet({ domain: domainName || '' });
      const domainUser = await getDomainUserBrickapiV1DomainsDomainUsersUserGet({
        domain: domainName || '',
        user: initialState?.currentUser?.name || '',
      });
      await setInitialState({
        ...initialState,
        currentDomain: domain.data,
        currentDomainUser: domainUser.data,
      });
    };
    if (domainName && domainName !== initialState?.currentDomain?.name) {
      setDomain();
    }
  });
  return domainName;
};
