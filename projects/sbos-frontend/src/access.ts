/**
 * @see https://umijs.org/docs/max/access#access
 * */
export default function access(
  initialState: { currentUser?: API.UserRead; currentDomainUser?: API.DomainUserRead } | undefined,
) {
  const { currentUser, currentDomainUser } = initialState ?? {};
  const isSiteAdmin = currentUser && currentUser.isSuperuser;
  const isDomainAdmin = isSiteAdmin || (currentDomainUser && currentDomainUser.isAdmin);
  return {
    isSiteAdmin,
    isDomainAdmin,
  };
}
