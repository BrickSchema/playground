// @ts-ignore
/* eslint-disable */
import { request } from '@umijs/max';

/** Oauth:Google.Bearer.Authorize GET /brickapi/v1/auth/bearer/google/authorize */
export async function oauthGoogleBearerAuthorizeBrickapiV1AuthBearerGoogleAuthorizeGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.oauthGoogleBearerAuthorizeBrickapiV1AuthBearerGoogleAuthorizeGetParams,
  options?: { [key: string]: any },
) {
  return request<API.OAuth2AuthorizeResponse>('/brickapi/v1/auth/bearer/google/authorize', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Oauth:Google.Bearer.Callback The response varies based on the authentication backend used. GET /brickapi/v1/auth/bearer/google/callback */
export async function oauthGoogleBearerCallbackBrickapiV1AuthBearerGoogleCallbackGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.oauthGoogleBearerCallbackBrickapiV1AuthBearerGoogleCallbackGetParams,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/bearer/google/callback', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Auth:Bearer.Login POST /brickapi/v1/auth/bearer/login */
export async function authBearerLoginBrickapiV1AuthBearerLoginPost(
  body: API.BodyAuthBearerLoginBrickapiV1AuthBearerLoginPost,
  options?: { [key: string]: any },
) {
  return request<API.BearerResponse>('/brickapi/v1/auth/bearer/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: body,
    ...(options || {}),
  });
}

/** Auth:Bearer.Logout POST /brickapi/v1/auth/bearer/logout */
export async function authBearerLogoutBrickapiV1AuthBearerLogoutPost(options?: {
  [key: string]: any;
}) {
  return request<any>('/brickapi/v1/auth/bearer/logout', {
    method: 'POST',
    ...(options || {}),
  });
}

/** Oauth:Google.Cookie.Authorize GET /brickapi/v1/auth/cookie/google/authorize */
export async function oauthGoogleCookieAuthorizeBrickapiV1AuthCookieGoogleAuthorizeGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.oauthGoogleCookieAuthorizeBrickapiV1AuthCookieGoogleAuthorizeGetParams,
  options?: { [key: string]: any },
) {
  return request<API.OAuth2AuthorizeResponse>('/brickapi/v1/auth/cookie/google/authorize', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Oauth:Google.Cookie.Callback The response varies based on the authentication backend used. GET /brickapi/v1/auth/cookie/google/callback */
export async function oauthGoogleCookieCallbackBrickapiV1AuthCookieGoogleCallbackGet(
  // 叠加生成的Param类型 (非body参数swagger默认没有生成对象)
  params: API.oauthGoogleCookieCallbackBrickapiV1AuthCookieGoogleCallbackGetParams,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/cookie/google/callback', {
    method: 'GET',
    params: {
      ...params,
    },
    ...(options || {}),
  });
}

/** Auth:Cookie.Login POST /brickapi/v1/auth/cookie/login */
export async function authCookieLoginBrickapiV1AuthCookieLoginPost(
  body: API.BodyAuthCookieLoginBrickapiV1AuthCookieLoginPost,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/cookie/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    data: body,
    ...(options || {}),
  });
}

/** Auth:Cookie.Logout POST /brickapi/v1/auth/cookie/logout */
export async function authCookieLogoutBrickapiV1AuthCookieLogoutPost(options?: {
  [key: string]: any;
}) {
  return request<any>('/brickapi/v1/auth/cookie/logout', {
    method: 'POST',
    ...(options || {}),
  });
}

/** Reset:Forgot Password POST /brickapi/v1/auth/forgot-password */
export async function resetForgotPasswordBrickapiV1AuthForgotPasswordPost(
  body: API.BodyResetForgotPasswordBrickapiV1AuthForgotPasswordPost,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/forgot-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Register:Register POST /brickapi/v1/auth/register */
export async function registerRegisterBrickapiV1AuthRegisterPost(
  body: API.UserCreate,
  options?: { [key: string]: any },
) {
  return request<API.UserReadResp>('/brickapi/v1/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Verify:Request-Token POST /brickapi/v1/auth/request-verify-token */
export async function verifyRequestTokenBrickapiV1AuthRequestVerifyTokenPost(
  body: API.BodyVerifyRequestTokenBrickapiV1AuthRequestVerifyTokenPost,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/request-verify-token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Reset:Reset Password POST /brickapi/v1/auth/reset-password */
export async function resetResetPasswordBrickapiV1AuthResetPasswordPost(
  body: API.BodyResetResetPasswordBrickapiV1AuthResetPasswordPost,
  options?: { [key: string]: any },
) {
  return request<any>('/brickapi/v1/auth/reset-password', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}

/** Verify:Verify POST /brickapi/v1/auth/verify */
export async function verifyVerifyBrickapiV1AuthVerifyPost(
  body: API.BodyVerifyVerifyBrickapiV1AuthVerifyPost,
  options?: { [key: string]: any },
) {
  return request<API.UserRead>('/brickapi/v1/auth/verify', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: body,
    ...(options || {}),
  });
}
