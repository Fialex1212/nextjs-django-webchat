"use client";

import Link from "next/link";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import toast, { Toaster } from "react-hot-toast";
import axios from "axios";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { useEffect } from "react";
import { useAuth } from "@/contexts/authContext";
import { useUserData } from "@/contexts/userContext";

const formSchema = z.object({
  email: z.string().email("Invalid email format"),
  password: z.string().min(8).max(50),
});

type FormData = z.infer<typeof formSchema>;

const SignIn = () => {
  const {token, updateToken} = useAuth();
  const { updateUserData } = useUserData();
  const router = useRouter();

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: FormData) => {
    console.log(data);
    try {
      const response =  await axios.post("http://localhost:8000/api/users/login/", data);
      const { access, user } = response.data;
      updateToken(access);
      updateUserData({ id: user.id, username: user.username, email: user.email });
      toast.success("Successfully signed in.");
      router.push("/");
    } catch (error) {
      toast.error("Something went wrong, check your inputs.");
      console.log(error);
    }
  };

  useEffect(() => {
    if (token) {
      router.push("/");
    }
  }, [token, router]);

  return (
    <main className="flex h-[calc(100vh-100px)] justify-center items-center">
      <Toaster />
      <Card className="mx-auto max-w-sm xs:border border-0">
        <CardHeader>
          <CardTitle className="text-xl">Sign In</CardTitle>
          <CardDescription>
            Enter your information to sign in to an account
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            <Form {...form}>
              <form className="grid gap-3" onSubmit={form.handleSubmit(onSubmit)}>
                <div className="grid gap-2">
                  <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Email</FormLabel>
                        <FormControl>
                          <Input placeholder="Email" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                </div>
                <div className="grid gap-2">
                  <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Password</FormLabel>
                        <FormControl>
                          <Input type="password" placeholder="Password" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <Button type="submit" className="w-full">
                    Create an account
                  </Button>
                  <Button variant="outline" className="w-full">
                    Sign up with GitHub
                  </Button>
                </div>
              </form>
            </Form>
          </div>
          <div className="mt-4 text-center text-sm">
            You have no account?
            <Link href="/auth/sign-up" className="underline">
              Sign up
            </Link>
          </div>
        </CardContent>
      </Card>
    </main>
  );
};

export default SignIn;
