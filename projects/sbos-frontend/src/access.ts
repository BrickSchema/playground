/**
 * @see https://umijs.org/docs/max/access#access
 * */
export default function access(
  initialState: { currentUser?: API.UserRead; currentDomainUser?: API.DomainUserRead } | undefined,
) {
  const { currentUser, currentDomainUser } = initialState ?? {};
  const isSiteAdmin: boolean = currentUser && currentUser.isSuperuser || false;
  const isDomainAdmin: boolean = isSiteAdmin || (currentDomainUser && currentDomainUser.isAdmin) || false;
  return {
    isSiteAdmin,
    isDomainAdmin,
  };
}
