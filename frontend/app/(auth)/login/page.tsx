"use client"
import { AuthButton } from "@/components/auth/AuthButton";
import { AuthCard } from "@/components/auth/AuthCard";
import { AuthInput } from "@/components/auth/AuthInput";
import Link from "next/link";
import { useActionState, useEffect } from "react"; // React 19 / Next.js 15
import { loginAction } from "../action";
import { useRouter } from "next/navigation";

export default function Login() {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const [state, formAction, isPending] = useActionState(loginAction, null as any);
    const router = useRouter();

    useEffect(() => {
        if (state?.success) {
            router.push("/dashboard");
        }
    }, [state?.success, router]);

    return (
        <AuthCard title="Welcome Back" subtitle="Log in to your dashboard account">
            <form action={formAction} className="mt-8 space-y-6">
                {state?.message && !state?.success && (
                    <div className="p-3 rounded-lg bg-red-50 border border-red-200 text-red-600 text-sm text-center font-medium shadow-sm">
                        {state.message}
                    </div>
                )}
                {state?.message && state?.success && (
                    <div className="p-3 rounded-lg bg-green-50 border border-green-200 text-green-600 text-sm text-center font-medium shadow-sm">
                        {state.message}
                    </div>
                    
                )}
                
                <div className="space-y-5">
                    <AuthInput 
                        label="Email Address"
                        type="email" 
                        name="email" 
                        placeholder="you@example.com" 
                        required 
                        disabled={isPending}
                        error={state?.errors?.email}
                    />
                    
                    <AuthInput 
                        label="Password"
                        type="password" 
                        name="password" 
                        placeholder="••••••••" 
                        required 
                        disabled={isPending}
                        error={state?.errors?.password}
                    />
                </div>

                <div className="flex items-center justify-between">
                    <div className="flex items-center">
                        <input
                            id="remember-me"
                            name="remember-me"
                            type="checkbox"
                            className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded cursor-pointer"
                        />
                        <label htmlFor="remember-me" className="ml-2 block text-sm text-gray-700 cursor-pointer">
                            Remember me
                        </label>
                    </div>

                    <div className="text-sm">
                        <a href="#" className="font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
                            Forgot your password?
                        </a>
                    </div>
                </div>

                <div className="pt-2">
                    <AuthButton type="submit" isLoading={isPending}>
                        Sign in
                    </AuthButton>
                </div>

                <p className="text-center text-sm text-gray-600 mt-6">
                    Don't have an account?{' '}
                    <Link href="/register" className="font-medium text-indigo-600 hover:text-indigo-500 transition-colors">
                        Create an account
                    </Link>
                </p>
            </form>       
        </AuthCard>
    )
}