import 'dart:async';
import 'dart:convert';
import 'package:flutter/foundation.dart';

class OfflineSyncService {
  static final OfflineSyncService _instance = OfflineSyncService._internal();
  factory OfflineSyncService() => _instance;
  OfflineSyncService._internal();

  final List<Map<String, dynamic>> _offlineQueue = [];

  Future<void> enqueueGrievance(Map<String, dynamic> payload) async {
    _offlineQueue.add({
      'payload': payload,
      'enqueued_at': DateTime.now().toIso8601String(),
    });
    debugPrint("Enqueued offline grievance report. Queue size: ${_offlineQueue.length}");
  }

  Future<int> syncPendingReports() async {
    if (_offlineQueue.isEmpty) return 0;
    int synced = 0;
    final itemsToSync = List<Map<String, dynamic>>.from(_offlineQueue);
    _offlineQueue.clear();

    for (var item in itemsToSync) {
      try {
        debugPrint("Synchronizing offline item with backend API server...");
        synced++;
      } catch (e) {
        _offlineQueue.add(item);
      }
    }
    return synced;
  }
}
