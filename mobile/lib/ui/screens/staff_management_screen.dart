import 'package:flutter/material.dart';

class StaffManagementScreen extends StatefulWidget {
  const StaffManagementScreen({super.key});

  @override
  State<StaffManagementScreen> createState() => _StaffManagementScreenState();
}

class _StaffManagementScreenState extends State<StaffManagementScreen> {
  final List<Map<String, dynamic>> _staffMembers = [
    {
      'name': 'Staff A',
      'department': 'Public Works',
      'active': 12,
      'pending': 4,
      'resolved': 38,
      'avg_resolution': 1.8,
      'status': 'Active'
    },
    {
      'name': 'Staff B',
      'department': 'Sanitation',
      'active': 5,
      'pending': 1,
      'resolved': 50,
      'avg_resolution': 0.9,
      'status': 'Active'
    },
    {
      'name': 'Staff C',
      'department': 'Water',
      'active': 0,
      'pending': 0,
      'resolved': 12,
      'avg_resolution': 3.2,
      'status': 'Disabled'
    },
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Staff Management'),
        actions: [
          IconButton(
            icon: const Icon(Icons.person_add),
            onPressed: () => _showAddEditStaffDialog(context),
          ),
        ],
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(16.0),
        itemCount: _staffMembers.length,
        itemBuilder: (context, index) {
          final staff = _staffMembers[index];
          final isActive = staff['status'] == 'Active';

          return Card(
            elevation: 2,
            margin: const EdgeInsets.only(bottom: 16.0),
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
            child: ExpansionTile(
              leading: CircleAvatar(
                backgroundColor: isActive ? Colors.blue : Colors.grey,
                child: const Icon(Icons.person, color: Colors.white),
              ),
              title: Text(staff['name'], style: TextStyle(
                fontWeight: FontWeight.bold,
                decoration: isActive ? TextDecoration.none : TextDecoration.lineThrough,
              )),
              subtitle: Text(staff['department']),
              children: [
                Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Text('Workload Overview', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                      const SizedBox(height: 12),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          _buildWorkloadStat('Active', '${staff['active']}', Colors.blue),
                          _buildWorkloadStat('Pending', '${staff['pending']}', Colors.orange),
                          _buildWorkloadStat('Resolved', '${staff['resolved']}', Colors.green),
                        ],
                      ),
                      const SizedBox(height: 16),
                      Text('Average Resolution: ${staff['avg_resolution']} days', style: const TextStyle(fontStyle: FontStyle.italic)),
                      const Divider(height: 32),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          OutlinedButton.icon(
                            onPressed: () => _showAddEditStaffDialog(context, staff: staff),
                            icon: const Icon(Icons.edit),
                            label: const Text('Edit'),
                          ),
                          OutlinedButton.icon(
                            onPressed: () {},
                            icon: Icon(isActive ? Icons.block : Icons.check_circle, color: isActive ? Colors.red : Colors.green),
                            label: Text(isActive ? 'Disable' : 'Enable', style: TextStyle(color: isActive ? Colors.red : Colors.green)),
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

  Widget _buildWorkloadStat(String label, String value, Color color) {
    return Column(
      children: [
        Text(value, style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20, color: color)),
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
      ],
    );
  }

  void _showAddEditStaffDialog(BuildContext context, {Map<String, dynamic>? staff}) {
    final isEditing = staff != null;
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(isEditing ? 'Edit Staff' : 'Add Staff'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              decoration: const InputDecoration(labelText: 'Staff Name'),
              controller: TextEditingController(text: isEditing ? staff['name'] : ''),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(labelText: 'Assign Department'),
              value: isEditing ? staff['department'] : null,
              items: ['Public Works', 'Sanitation', 'Water', 'Electricity', 'Road']
                  .map((d) => DropdownMenuItem(value: d, child: Text(d)))
                  .toList(),
              onChanged: (val) {},
            ),
          ],
        ),
        actions: [
          TextButton(onPressed: () => Navigator.pop(context), child: const Text('Cancel')),
          ElevatedButton(onPressed: () => Navigator.pop(context), child: Text(isEditing ? 'Save' : 'Add')),
        ],
      ),
    );
  }
}
