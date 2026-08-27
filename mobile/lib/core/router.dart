import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// Import screens when created
import '../ui/screens/splash_screen.dart';
import '../ui/screens/login_screen.dart';
import '../ui/screens/home_screen.dart';
import '../ui/screens/report_problem_screen.dart';

final GoRouter appRouter = GoRouter(
  initialLocation: '/',
  routes: [
    GoRoute(
      path: '/',
      name: 'splash',
      builder: (context, state) => const SplashScreen(),
    ),
    GoRoute(
      path: '/login',
      name: 'login',
      builder: (context, state) => const LoginScreen(),
    ),
    GoRoute(
      path: '/home',
      name: 'home',
      builder: (context, state) => const HomeScreen(),
    ),
    GoRoute(
      path: '/report',
      name: 'report',
      builder: (context, state) => const ReportProblemScreen(),
    ),
  ],
);
