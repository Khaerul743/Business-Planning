"use server"

import { logger } from "@/lib/logger";
import { authService } from "@/lib/services/auth/authService";
import { loginSchema, registerSchema } from "@/lib/services/auth/types";
import { cookies } from "next/headers";

export type ActionResponse = {
  success: boolean;
  message: string;
  errors?: Record<string, string[]>;
};

export async function registerAction(prevData: ActionResponse | null, formData: FormData): Promise<ActionResponse> {
  const rawData = Object.fromEntries(formData.entries());
  const validatedFields = registerSchema.safeParse(rawData)

  if (!validatedFields.success) {
    logger.warn("Validation failed")
    return {
      success: false,
      message: "Validation failed",
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    const res = await authService.register(validatedFields.data)
    if (res.status !== "success") {
      logger.warn(`User registration failed with email ${validatedFields.data.email}`)
      return {
        success: false,
        message: res.message,
      }
    }

    logger.info(`User registration is successfully with email ${validatedFields.data.email}`)
    return {
      success: true,
      message: res.message
    }

  } catch (error) {
    logger.error(`Unexpected error while execute register action: ${error}`)
    return {
      success: false,
      message: "Internal server error, please try again later"
    }
  }
}

export async function loginAction(prevData: ActionResponse | null, formData: FormData): Promise<ActionResponse> {
  const rawData = Object.fromEntries(formData.entries());
  const validatedFields = loginSchema.safeParse(rawData)
  if (!validatedFields.success) {
    logger.warn("Validation Failed")
    return {
      success: false,
      message: "Validation failed",
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  try {
    const res = await authService.login(validatedFields.data)
    console.log(res)
    if (res.status !== "success") {
      logger.warn(`User login is failed with email ${validatedFields.data.email}`)
      return {
        success: false,
        message: res.message
      }
    }

    //Set Cookie
    const cookieStore = await cookies()

    cookieStore.set("access_token", res.data.access_token, {
      httpOnly: true,
      secure: false,
      sameSite: "lax",
      path: "/",
      maxAge: 3600
    })

    cookieStore.set("refresh_token", res.data.refresh_token, {
      httpOnly: true,
      secure: false,
      sameSite: "lax",
      path: "/",
      maxAge: 60 * 60 * 24 * 7
    })

    logger.info(`User login is successfully with email ${validatedFields.data.email}`)
    return {
      success: true,
      message: res.message
    }
  } catch (error) {
    logger.error(`Unexpected error while execute register action: ${error}`)
    return {
      success: false,
      message: "Internal server error, please try again later"
    }
  }
}