import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

// Import screens when created
import '../ui/screens/splash_screen.dart';
import '../ui/screens/login_screen.dart';
import '../ui/screens/home_screen.dart';
import '../ui/screens/report_problem_screen.dart';
import '../ui/screens/complaint_detail_screen.dart';
import '../ui/screens/admin_dashboard_screen.dart';
import '../ui/screens/department_management_screen.dart';
import '../ui/screens/staff_management_screen.dart';

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
    GoRoute(
      path: '/complaint/:id',
      name: 'complaint_detail',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return ComplaintDetailScreen(complaintId: id);
      },
    ),
    GoRoute(
      path: '/admin',
      name: 'admin',
      builder: (context, state) => const AdminDashboardScreen(),
    ),
    GoRoute(
      path: '/admin/departments',
      name: 'departments',
      builder: (context, state) => const DepartmentManagementScreen(),
    ),
    GoRoute(
      path: '/admin/staff',
      name: 'staff',
      builder: (context, state) => const StaffManagementScreen(),
    ),
  ],
);
