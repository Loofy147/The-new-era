import { StackServerApp, StackClientApp } from "@stackframe/stack";

export const stackServerApp = new StackServerApp({
  tokenStore: "nextjs-cookie", // Store tokens in Next.js cookies
  urls: {
    signIn: "/auth/signin",
    signUp: "/auth/signup", 
    afterSignIn: "/dashboard",
    afterSignUp: "/dashboard",
    afterSignOut: "/",
    home: "/",
    emailVerification: "/auth/email-verification",
    passwordReset: "/auth/password-reset",
    magicLinkCallback: "/auth/magic-link",
    oauthCallback: "/auth/oauth-callback",
  },
});

export const stackClientApp = new StackClientApp({
  baseUrl: process.env.NEXT_PUBLIC_STACK_BASE_URL,
  projectId: process.env.NEXT_PUBLIC_STACK_PROJECT_ID!,
  publishableClientKey: process.env.NEXT_PUBLIC_STACK_PUBLISHABLE_CLIENT_KEY!,
  tokenStore: "nextjs-cookie",
  urls: {
    signIn: "/auth/signin",
    signUp: "/auth/signup",
    afterSignIn: "/dashboard", 
    afterSignUp: "/dashboard",
    afterSignOut: "/",
    home: "/",
    emailVerification: "/auth/email-verification",
    passwordReset: "/auth/password-reset",
    magicLinkCallback: "/auth/magic-link",
    oauthCallback: "/auth/oauth-callback",
  },
});
