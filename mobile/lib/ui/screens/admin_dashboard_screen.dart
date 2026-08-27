import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AdminDashboardScreen extends StatefulWidget {
  const AdminDashboardScreen({super.key});

  @override
  State<AdminDashboardScreen> createState() => _AdminDashboardScreenState();
}

class _AdminDashboardScreenState extends State<AdminDashboardScreen> {
  final List<Map<String, dynamic>> _mockComplaints = [
    {'id': 'CC-2026-1001', 'category': 'Pothole', 'status': 'SUBMITTED', 'priority': 'HIGH', 'date': '2026-08-27'},
    {'id': 'CC-2026-1002', 'category': 'Streetlight', 'status': 'IN_PROGRESS', 'priority': 'MEDIUM', 'date': '2026-08-26'},
    {'id': 'CC-2026-1003', 'category': 'Water Leak', 'status': 'ESCALATED', 'priority': 'CRITICAL', 'date': '2026-08-25'},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Admin Dashboard'),
        actions: [
          IconButton(icon: const Icon(Icons.business), onPressed: () => context.push('/admin/departments')),
          IconButton(icon: const Icon(Icons.settings), onPressed: () {}),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildMetricsGrid(context),
            const SizedBox(height: 32),
            _buildManagementSection(context),
          ],
        ),
      ),
    );
  }

  Widget _buildMetricsGrid(BuildContext context) {
    return GridView.count(
      crossAxisCount: 2,
      crossAxisSpacing: 12,
      mainAxisSpacing: 12,
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      childAspectRatio: 2.0,
      children: [
        _buildMetricCard(context, 'Total Complaints', '1,245', Colors.blue),
        _buildMetricCard(context, 'New Complaints', '24', Colors.purple),
        _buildMetricCard(context, 'Pending', '45', Colors.orange),
        _buildMetricCard(context, 'In Progress', '112', Colors.lightBlue),
        _buildMetricCard(context, 'Resolved', '1,050', Colors.green),
        _buildMetricCard(context, 'Escalated', '8', Colors.red),
        _buildMetricCard(context, 'Overdue', '6', Colors.brown),
      ],
    );
  }

  Widget _buildMetricCard(BuildContext context, String title, String value, Color color) {
    return Card(
      elevation: 2,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      child: Padding(
        padding: const EdgeInsets.all(12.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(value, style: Theme.of(context).textTheme.headlineSmall?.copyWith(color: color, fontWeight: FontWeight.bold)),
            Text(title, style: const TextStyle(fontSize: 12, color: Colors.grey), textAlign: TextAlign.center),
          ],
        ),
      ),
    );
  }

  Widget _buildManagementSection(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text('Manage Complaints', style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
            Row(
              children: [
                IconButton(icon: const Icon(Icons.search), onPressed: () {}),
                IconButton(icon: const Icon(Icons.filter_list), onPressed: () {}),
                IconButton(icon: const Icon(Icons.sort), onPressed: () {}),
              ],
            )
          ],
        ),
        const SizedBox(height: 16),
        ListView.builder(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          itemCount: _mockComplaints.length,
          itemBuilder: (context, index) {
            final complaint = _mockComplaints[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              child: ListTile(
                title: Text('${complaint['id']} - ${complaint['category']}', style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text('Status: ${complaint['status']} | Priority: ${complaint['priority']}'),
                trailing: const Icon(Icons.more_vert),
                onTap: () => _showManagementBottomSheet(context, complaint),
              ),
            );
          },
        ),
      ],
    );
  }

  void _showManagementBottomSheet(BuildContext context, Map<String, dynamic> complaint) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Manage ${complaint['id']}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                ListTile(
                  leading: const Icon(Icons.person_add, color: Colors.blue),
                  title: const Text('Assign Staff'),
                  onTap: () => Navigator.pop(context),
                ),
                ListTile(
                  leading: const Icon(Icons.edit, color: Colors.orange),
                  title: const Text('Change Status / Priority'),
                  onTap: () => Navigator.pop(context),
                ),
                ListTile(
                  leading: const Icon(Icons.warning, color: Colors.red),
                  title: const Text('Escalate'),
                  onTap: () => Navigator.pop(context),
                ),
                ListTile(
                  leading: const Icon(Icons.note_add, color: Colors.green),
                  title: const Text('Add Internal Note'),
                  onTap: () => Navigator.pop(context),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
