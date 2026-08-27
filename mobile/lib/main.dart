import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/theme.dart';
import 'core/router.dart';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'services/offline_sync_manager.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Offline Sync Listener
  Connectivity().onConnectivityChanged.listen((List<ConnectivityResult> results) {
    if (results.contains(ConnectivityResult.mobile) || results.contains(ConnectivityResult.wifi)) {
      OfflineSyncManager().syncOfflineData();
    }
  });

  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Civic Connect',
      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      routerConfig: appRouter,
    );
  }
}
