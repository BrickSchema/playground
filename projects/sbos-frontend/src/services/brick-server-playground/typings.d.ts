declare namespace API {
  type ActuationResult = {
    /** Success */
    success: boolean;
    /** Detail */
    detail?: string;
  };

  type ActuationResults = {
    /** Results */
    results?: ActuationResult[];
    /** Responsetime */
    responseTime?: Record<string, any>;
  };

  type ActuationResultsResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: ActuationResults | null;
  };

  type addDomainUserBrickapiV1DomainsDomainUsersUserPostParams = {
    domain: string;
    user: string;
  };

  type addDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesPostParams = {
    domain: string;
    user: string;
  };

  type AppBuild = {
    /** Stdout */
    stdout: string;
    /** Stderr */
    stderr: string;
    /** Returncode */
    returncode: number;
  };

  type AppBuildResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AppBuild | null;
  };

  type AppCreate = {
    /** Name */
    name: string;
    /** Description */
    description?: string;
  };

  type AppData = {
    permissionProfile?: PermissionProfileRead | null;
    permissionModel?: PermissionModel;
    /** Frontend */
    frontend?: string | null;
    /** Backend */
    backend?: string | null;
  };

  type AppRead = {
    /** Id */
    id: string;
    /** Name */
    name: string;
    /** Description */
    description: string;
    /** Approved */
    approved: boolean;
  };

  type AppReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: AppRead[];
  };

  type AppReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AppReadList | null;
  };

  type AppReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AppRead | null;
  };

  type AppReadWithAllData = {
    /** Id */
    id: string;
    /** Name */
    name: string;
    /** Description */
    description: string;
    /** Approved */
    approved: boolean;
    approvedData?: AppData | null;
    submittedData?: AppData | null;
  };

  type AppReadWithAllDataResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AppReadWithAllData | null;
  };

  type AppReadWithApprovedData = {
    /** Id */
    id: string;
    /** Name */
    name: string;
    /** Description */
    description: string;
    /** Approved */
    approved: boolean;
    approvedData?: AppData | null;
  };

  type AppReadWithApprovedDataResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AppReadWithApprovedData | null;
  };

  type appsApiBrickapiV1AppsAppApiPathGetParams = {
    /** Api endpoint in the app */
    path: string;
  };

  type appsApiBrickapiV1AppsAppApiPathGetParams = {
    /** Api endpoint in the app */
    path: string;
  };

  type appsApiBrickapiV1AppsAppApiPathGetParams = {
    /** Api endpoint in the app */
    path: string;
  };

  type appsApiBrickapiV1AppsAppApiPathGetParams = {
    /** Api endpoint in the app */
    path: string;
  };

  type appsApiBrickapiV1AppsAppApiPathGetParams = {
    /** Api endpoint in the app */
    path: string;
  };

  type appsApproveBrickapiV1AppsAppApprovePostParams = {
    app: string;
  };

  type appsBuildBrickapiV1AppsAppBuildPostParams = {
    app: string;
  };

  type appsDeleteBrickapiV1AppsAppDeleteParams = {
    app: string;
  };

  type appsGetBrickapiV1AppsAppGetParams = {
    app: string;
  };

  type appsStaticBrickapiV1AppsAppStaticPathGetParams = {
    /** TODO */
    app: string;
    /** TODO */
    path: string;
  };

  type appsSubmitDataBrickapiV1AppsAppSubmitPostParams = {
    app: string;
  };

  type AuthorizedEntities = {
    /** Read */
    read: Record<string, any>;
    /** Write */
    write: Record<string, any>;
    /** Isadmin */
    isAdmin?: boolean;
    /** Responsetime */
    responseTime?: number;
  };

  type AuthorizedEntitiesResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: AuthorizedEntities | null;
  };

  type BearerResponse = {
    /** Access Token */
    access_token: string;
    /** Token Type */
    token_type: string;
  };

  type BodyAppsSubmitDataBrickapiV1Apps_app_submitPost = {
    /** Frontend File */
    frontend_file?: string;
    /** Backend File */
    backend_file?: string;
    /** Permission Profile Read */
    permission_profile_read: string;
    /** Permission Profile Write */
    permission_profile_write: string;
    /** Permission Profile Arguments */
    permission_profile_arguments: string;
    permission_model: PermissionModel;
  };

  type BodyAuthBearerLoginBrickapiV1AuthBearerLoginPost = {
    /** Grant Type */
    grant_type?: string | null;
    /** Username */
    username: string;
    /** Password */
    password: string;
    /** Scope */
    scope?: string;
    /** Client Id */
    client_id?: string | null;
    /** Client Secret */
    client_secret?: string | null;
  };

  type BodyAuthCookieLoginBrickapiV1AuthCookieLoginPost = {
    /** Grant Type */
    grant_type?: string | null;
    /** Username */
    username: string;
    /** Password */
    password: string;
    /** Scope */
    scope?: string;
    /** Client Id */
    client_id?: string | null;
    /** Client Secret */
    client_secret?: string | null;
  };

  type BodyResetForgotPasswordBrickapiV1AuthForgotPasswordPost = {
    /** Email */
    email: string;
  };

  type BodyResetResetPasswordBrickapiV1AuthResetPasswordPost = {
    /** Token */
    token: string;
    /** Password */
    password: string;
  };

  type BodyUploadTurtleFileBrickapiV1Domains_domain_uploadPost = {
    /** File */
    file: string;
  };

  type BodyVerifyRequestTokenBrickapiV1AuthRequestVerifyTokenPost = {
    /** Email */
    email: string;
  };

  type BodyVerifyVerifyBrickapiV1AuthVerifyPost = {
    /** Token */
    token: string;
  };

  type ColumnType = 'number' | 'text' | 'loc' | 'uuid' | 'timestamp';

  type createDomainBrickapiV1DomainsDomainPostParams = {
    domain: string;
  };

  type createDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPostParams = {
    domain: string;
  };

  type deleteBrickapiV1DataTimeseriesDomainsDomainDeleteParams = {
    domain: string;
    entity_id: string;
    /** Starting time of the data in UNIX timestamp in seconds (float). If not given, the beginning of the data will be assumed. */
    start_time?: number;
    /** Ending time of the data in UNIX timestamp in seconds (float). If not given, the end of the data will be assumed. */
    end_time?: number;
  };

  type deleteDomainBrickapiV1DomainsDomainDeleteParams = {
    domain: string;
  };

  type deleteDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyDeleteParams = {
    domain: string;
    /** ObjectId of the domain pre actuation policy */
    policy: string;
  };

  type deleteDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfileDeleteParams = {
    domain: string;
    user: string;
    /** ObjectId of the permission profile */
    profile: string;
  };

  type deleteResourceBrickapiV1DomainsDomainResourcesEntityIdDeleteParams = {
    entity_id: string;
    domain: string;
  };

  type dictResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    /** Data */
    data?: Record<string, any> | null;
  };

  type DomainAppRead = {
    /** Id */
    id: string;
    domain: DomainRead;
    app: AppRead;
  };

  type DomainAppReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainAppRead[];
  };

  type DomainAppReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainAppReadList | null;
  };

  type DomainAppReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainAppRead | null;
  };

  type domainApproveAppBrickapiV1DomainsDomainAppsAppPostParams = {
    domain: string;
    app: string;
  };

  type domainGetAppBrickapiV1DomainsDomainAppsAppGetParams = {
    domain: string;
    app: string;
  };

  type domainListAppBrickapiV1DomainsDomainAppsGetParams = {
    domain: string;
  };

  type DomainPreActuationPolicyCreate = {
    /** Name */
    name: string;
    /** Query */
    query?: string;
    /** Priority */
    priority?: number;
    /** Guards */
    guards?: string[];
  };

  type DomainPreActuationPolicyRead = {
    /** Id */
    id: string;
    domain: DomainRead;
    /** Name */
    name: string;
    /** Query */
    query: string;
    /** Priority */
    priority: number;
    /** Guards */
    guards: string[];
  };

  type DomainPreActuationPolicyReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainPreActuationPolicyRead[];
  };

  type DomainPreActuationPolicyReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainPreActuationPolicyReadList | null;
  };

  type DomainPreActuationPolicyReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainPreActuationPolicyRead | null;
  };

  type DomainPreActuationPolicyUpdate = {
    /** Name */
    name?: string | null;
    /** Query */
    query?: string | null;
    /** Priority */
    priority?: number | null;
    /** Guards */
    guards?: string[] | null;
  };

  type DomainRead = {
    /** Id */
    id: string;
    /** Name */
    name: string;
    /** Initialized */
    initialized: boolean;
  };

  type DomainReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainRead[];
  };

  type DomainReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainReadList | null;
  };

  type DomainReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainRead | null;
  };

  type DomainUserAppArguments = {
    /** Arguments */
    arguments?: Record<string, any>;
  };

  type DomainUserAppRead = {
    /** Id */
    id: string;
    domain: DomainRead;
    user: UserRead;
    app: AppRead;
    /** Status */
    status: string;
    /** Containerid */
    containerId: string;
    /** Arguments */
    arguments: Record<string, any>;
    /** Token */
    token: string;
  };

  type DomainUserAppReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainUserAppRead[];
  };

  type DomainUserAppReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserAppReadList | null;
  };

  type DomainUserAppReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserAppRead | null;
  };

  type DomainUserProfileCreate = {
    /** Profile */
    profile: string;
    /** Arguments */
    arguments?: Record<string, any>;
  };

  type DomainUserProfileRead = {
    /** Id */
    id: string;
    domain: DomainRead;
    user: UserRead;
    profile: PermissionProfileRead;
    /** Arguments */
    arguments: Record<string, any>;
  };

  type DomainUserProfileReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainUserProfileRead[];
  };

  type DomainUserProfileReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserProfileReadList | null;
  };

  type DomainUserProfileReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserProfileRead | null;
  };

  type DomainUserProfileUpdate = {
    /** Arguments */
    arguments: Record<string, any>;
  };

  type DomainUserRead = {
    /** Id */
    id: string;
    domain: DomainRead;
    user: UserRead;
    /** Isadmin */
    isAdmin?: boolean;
  };

  type DomainUserReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: DomainUserRead[];
  };

  type DomainUserReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserReadList | null;
  };

  type DomainUserReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: DomainUserRead | null;
  };

  type Empty = {};

  type EmptyResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: Empty | null;
  };

  type ErrorCode =
    | 'Success'
    | 'Error'
    | 'UnauthorizedError'
    | 'PermissionError'
    | 'InternalServerError'
    | 'InvalidTokenError'
    | 'UnknownFieldError'
    | 'IllegalFieldError'
    | 'IntegrityError'
    | 'ValidationError'
    | 'ApiNotImplementedError'
    | 'UserManagerError'
    | 'UserNotFoundError'
    | 'UserInvalidPasswordError'
    | 'UserAlreadyExistsError'
    | 'UserNotUpdatableError'
    | 'UserEmailAlreadyExistsError'
    | 'UserAlreadyVerifiedError'
    | 'UserInactiveError'
    | 'DomainNotFoundError'
    | 'DomainAlreadyExistsError'
    | 'GraphDBError'
    | 'ActuationDriverNotFoundError'
    | 'TimeseriesDriverNotFoundError';

  type ErrorModel = {
    /** Detail */
    detail: string | Record<string, any>;
  };

  type ErrorShowType = 0 | 1 | 2 | 3 | 9;

  type getBrickapiV1DataTimeseriesDomainsDomainGetParams = {
    domain: string;
    entity_id: string;
    /** Starting time of the data in UNIX timestamp in seconds (float). If not given, the beginning of the data will be assumed. */
    start_time?: number;
    /** Ending time of the data in UNIX timestamp in seconds (float). If not given, the end of the data will be assumed. */
    end_time?: number;
    /** The type of value. Currently, there are numbers (for both floating points and integers), texts, and locations (blobs are under dev.) */
    value_types?: ValueType[];
    offset?: number;
    limit?: number;
  };

  type getDomainBrickapiV1DomainsDomainGetParams = {
    domain: string;
  };

  type getDomainUserBrickapiV1DomainsDomainUsersUserGetParams = {
    domain: string;
    user: string;
  };

  type getProfileBrickapiV1ProfilesProfileGetParams = {
    /** ObjectId of the permission profile */
    profile: string;
  };

  type HTTPValidationError = {
    /** Detail */
    detail?: ValidationError[];
  };

  type initDomainBrickapiV1DomainsDomainInitGetParams = {
    domain: string;
  };

  type listDomainPreActuationPoliciesBrickapiV1DomainsDomainPoliciesGetParams = {
    domain: string;
  };

  type listDomainUserBrickapiV1DomainsDomainUsersGetParams = {
    domain: string;
  };

  type listDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesGetParams = {
    domain: string;
    user: string;
  };

  type listResourcesBrickapiV1DomainsDomainResourcesGetParams = {
    domain: string;
  };

  type notifyResourceBrickapiV1DomainsDomainResourcesEntityIdNotifyPostParams = {
    entity_id: string;
    domain: string;
  };

  type OAuth2AuthorizeResponse = {
    /** Authorization Url */
    authorization_url: string;
  };

  type oauthGoogleBearerAuthorizeBrickapiV1AuthBearerGoogleAuthorizeGetParams = {
    scopes?: string[];
  };

  type oauthGoogleBearerCallbackBrickapiV1AuthBearerGoogleCallbackGetParams = {
    code?: string | null;
    code_verifier?: string | null;
    state?: string | null;
    error?: string | null;
  };

  type oauthGoogleCookieAuthorizeBrickapiV1AuthCookieGoogleAuthorizeGetParams = {
    scopes?: string[];
  };

  type oauthGoogleCookieCallbackBrickapiV1AuthCookieGoogleCallbackGetParams = {
    code?: string | null;
    code_verifier?: string | null;
    state?: string | null;
    error?: string | null;
  };

  type PermissionModel = 'intersection' | 'augmentation';

  type PermissionProfileCreate = {
    /** Name */
    name: string;
    /** Read */
    read: string;
    /** Write */
    write: string;
    /** Arguments */
    arguments: Record<string, any>;
  };

  type PermissionProfileRead = {
    /** Id */
    id: string;
    /** Name */
    name?: string;
    /** Read */
    read: string;
    /** Write */
    write: string;
    /** Arguments */
    arguments: Record<string, any>;
  };

  type PermissionProfileReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: PermissionProfileRead[];
  };

  type PermissionProfileReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: PermissionProfileReadList | null;
  };

  type PermissionProfileReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: PermissionProfileRead | null;
  };

  type PermissionProfileUpdate = {
    /** Name */
    name?: string | null;
    /** Read */
    read?: string | null;
    /** Write */
    write?: string | null;
    /** Arguments */
    arguments?: Record<string, any> | null;
  };

  type postBrickapiV1ActuationDomainsDomainPostParams = {
    domain: string;
  };

  type postBrickapiV1DataTimeseriesDomainsDomainPostParams = {
    domain: string;
    entity_id: string;
  };

  type postBrickapiV1DomainsDomainSparqlPostParams = {
    domain: string;
  };

  type ResourceConstraintRead = {
    /** Entityid */
    entityId: string;
    /** Value */
    value: number;
  };

  type ResourceConstraintReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: ResourceConstraintRead[];
  };

  type ResourceConstraintReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: ResourceConstraintReadList | null;
  };

  type ResourceConstraintReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: ResourceConstraintRead | null;
  };

  type ResourceConstraintUpdate = {
    /** Value */
    value: number;
  };

  type strList = {
    /** Count */
    count?: number;
    /** Results */
    results?: string[];
  };

  type strListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: strList | null;
  };

  type TimeseriesData = {
    /** Data */
    data: any[][];
    /** Columns */
    columns?: ColumnType[];
  };

  type TimeseriesDataResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: TimeseriesData | null;
  };

  type updateDomainPreActuationPolicyBrickapiV1DomainsDomainPoliciesPolicyPatchParams = {
    domain: string;
    /** ObjectId of the domain pre actuation policy */
    policy: string;
  };

  type updateDomainUserProfileBrickapiV1DomainsDomainUsersUserProfilesProfilePatchParams = {
    domain: string;
    user: string;
    /** ObjectId of the permission profile */
    profile: string;
  };

  type updateProfileBrickapiV1ProfilesProfilePostParams = {
    /** ObjectId of the permission profile */
    profile: string;
  };

  type updateResourceBrickapiV1DomainsDomainResourcesEntityIdPostParams = {
    entity_id: string;
    domain: string;
  };

  type uploadTurtleFileBrickapiV1DomainsDomainUploadPostParams = {
    domain: string;
  };

  type UserCreate = {
    /** Email */
    email: string;
    /** Password */
    password: string;
    /** Isactive */
    isActive?: boolean | null;
    /** Issuperuser */
    isSuperuser?: boolean | null;
    /** Isverified */
    isVerified?: boolean | null;
    /** Name */
    name: string;
  };

  type UserRead = {
    /** Id */
    id: string;
    /** Email */
    email: string;
    /** Isactive */
    isActive?: boolean;
    /** Issuperuser */
    isSuperuser?: boolean;
    /** Isverified */
    isVerified?: boolean;
    /** Name */
    name: string;
  };

  type UserReadList = {
    /** Count */
    count?: number;
    /** Results */
    results?: UserRead[];
  };

  type UserReadListResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: UserReadList | null;
  };

  type UserReadResp = {
    errorCode: ErrorCode;
    /** Errormessage */
    errorMessage?: string;
    showType?: ErrorShowType;
    data?: UserRead | null;
  };

  type usersCreateAppContainerBrickapiV1UsersDomainsDomainAppsAppCreatePostParams = {
    domain: string;
    app: string;
  };

  type usersDeleteUserBrickapiV1UsersUserDeleteParams = {
    user: string;
  };

  type usersGetAppBrickapiV1UsersDomainsDomainAppsAppGetParams = {
    domain: string;
    app: string;
  };

  type usersInstallAppBrickapiV1UsersDomainsDomainAppsAppPostParams = {
    domain: string;
    app: string;
  };

  type usersListAppsBrickapiV1UsersDomainsDomainAppsGetParams = {
    domain: string;
  };

  type usersListDomainPermissionsBrickapiV1UsersDomainsDomainPermissionsGetParams = {
    domain: string;
    types?: string[];
  };

  type usersListDomainUserProfilesBrickapiV1UsersDomainsDomainProfilesGetParams = {
    domain: string;
  };

  type usersPatchUserBrickapiV1UsersUserPatchParams = {
    user: string;
  };

  type usersRemoveAppContainerBrickapiV1UsersDomainsDomainAppsAppRemovePostParams = {
    domain: string;
    app: string;
  };

  type usersSetAppArgumentsBrickapiV1UsersDomainsDomainAppsAppPatchParams = {
    domain: string;
    app: string;
  };

  type usersStartAppContainerBrickapiV1UsersDomainsDomainAppsAppStartPostParams = {
    domain: string;
    app: string;
  };

  type usersStopAppContainerBrickapiV1UsersDomainsDomainAppsAppStopPostParams = {
    domain: string;
    app: string;
  };

  type usersUninstallAppBrickapiV1UsersDomainsDomainAppsAppDeleteParams = {
    domain: string;
    app: string;
  };

  type usersUserBrickapiV1UsersUserGetParams = {
    user: string;
  };

  type UserUpdate = {
    /** Password */
    password?: string | null;
    /** Email */
    email?: string | null;
    /** Isactive */
    isActive?: boolean | null;
    /** Issuperuser */
    isSuperuser?: boolean | null;
    /** Isverified */
    isVerified?: boolean | null;
    /** Name */
    name?: string | null;
  };

  type ValidationError = {
    /** Location */
    loc: (string | number)[];
    /** Message */
    msg: string;
    /** Error Type */
    type: string;
  };

  type ValueType = 'number' | 'text' | 'loc';
}
