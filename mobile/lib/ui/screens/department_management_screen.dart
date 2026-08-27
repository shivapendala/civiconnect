import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class DepartmentManagementScreen extends StatefulWidget {
  const DepartmentManagementScreen({super.key});

  @override
  State<DepartmentManagementScreen> createState() => _DepartmentManagementScreenState();
}

class _DepartmentManagementScreenState extends State<DepartmentManagementScreen> {
  final List<Map<String, dynamic>> _departments = [
    {'name': 'Water', 'manager': 'Alice Smith', 'staff_count': 12, 'sla': 95.0, 'avg_time': 24},
    {'name': 'Electricity', 'manager': 'Bob Jones', 'staff_count': 20, 'sla': 88.5, 'avg_time': 48},
    {'name': 'Road', 'manager': 'Charlie Davis', 'staff_count': 15, 'sla': 72.0, 'avg_time': 120},
    {'name': 'Sanitation', 'manager': 'Diana Prince', 'staff_count': 30, 'sla': 98.2, 'avg_time': 12},
    {'name': 'Public Safety', 'manager': 'Evan Wright', 'staff_count': 40, 'sla': 99.9, 'avg_time': 4},
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Department Management'),
        actions: [
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: () => _showAddDepartmentDialog(context),
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: _departments.length,
        itemBuilder: (context, index) {
          final dept = _departments[index];
          return Card(
            elevation: 2,
            margin: const EdgeInsets.only(bottom: 16.0),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ExpansionTile(
              leading: const CircleAvatar(child: Icon(Icons.business)),
              title: Text(dept['name'], style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('Manager: ${dept['manager']}'),
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          _buildStatColumn('Staff', '${dept['staff_count']}'),
                          _buildStatColumn('SLA Rate', '${dept['sla']}%'),
                          _buildStatColumn('Avg Time', '${dept['avg_time']}h'),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          OutlinedButton.icon(
                            onPressed: () {},
                            icon: const Icon(Icons.edit),
                            label: const Text('Edit'),
                          ),
                          OutlinedButton.icon(
                            onPressed: () {},
                            icon: const Icon(Icons.rule),
                            label: const Text('SLA Rules'),
                          ),
                          OutlinedButton.icon(
                            onPressed: () {},
                            icon: const Icon(Icons.people),
                            label: const Text('Staff'),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildStatColumn(String label, String value) {
    return Column(
      children: [
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, color: Colors.blue)),
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
      ],
    );
  }

  void _showAddDepartmentDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('New Department'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(decoration: InputDecoration(labelText: 'Department Name')),
            SizedBox(height: 16),
            TextField(decoration: InputDecoration(labelText: 'Manager Name')),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: const Text('Create')),
        ],
      ),
    );
  }
}
