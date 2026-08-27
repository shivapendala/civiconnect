import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class NotificationsScreen extends StatelessWidget {
  const NotificationsScreen({super.key});

  final List<Map<String, dynamic>> _mockNotifications = const [
    {'title': 'Complaint Resolved', 'body': 'Your complaint CC-2026-1001 has been resolved by Public Works.', 'time': '2 hours ago', 'is_read': false},
    {'title': 'Complaint Assigned', 'body': 'Staff A has been assigned to investigate CC-2026-1002.', 'time': '1 day ago', 'is_read': true},
    {'title': 'Complaint Submitted', 'body': 'Thank you! Your complaint CC-2026-1002 was received.', 'time': '2 days ago', 'is_read': true},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Notifications'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => context.push('/notifications/preferences'),
          ),
        ],
      ),
      body: ListView.separated(
        itemCount: _mockNotifications.length,
        separatorBuilder: (context, index) => const Divider(height: 1),
        itemBuilder: (context, index) {
          final notif = _mockNotifications[index];
          final isRead = notif['is_read'] as bool;
          
          return Container(
            color: isRead ? Colors.transparent : Colors.blue.withOpacity(0.05),
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: isRead ? Colors.grey.shade200 : Colors.blue.shade100,
                child: Icon(
                  isRead ? Icons.notifications_none : Icons.notifications_active,
                  color: isRead ? Colors.grey : Colors.blue,
                ),
              ),
              title: Text(notif['title'], style: TextStyle(fontWeight: isRead ? FontWeight.normal : FontWeight.bold)),
              subtitle: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 4),
                  Text(notif['body']),
                  const SizedBox(height: 4),
                  Text(notif['time'], style: const TextStyle(fontSize: 12, color: Colors.grey)),
                ],
              ),
              isThreeLine: true,
              onTap: () {
                // Navigate to related complaint
              },
            ),
          );
        },
      ),
    );
  }
}
