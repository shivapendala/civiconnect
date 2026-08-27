import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:go_router/go_router.dart';

class AdminMapScreen extends StatefulWidget {
  const AdminMapScreen({super.key});

  @override
  State<AdminMapScreen> createState() => _AdminMapScreenState();
}

class _AdminMapScreenState extends State<AdminMapScreen> {
  final MapController _mapController = MapController();
  final LatLng _cityCenter = const LatLng(37.7749, -122.4194);

  // Mock data representing clustered or individual issues
  final List<Map<String, dynamic>> _adminIssues = [
    {'point': const LatLng(37.7750, -122.4180), 'priority': 'HIGH', 'id': 'CC-1001'},
    {'point': const LatLng(37.7760, -122.4210), 'priority': 'CRITICAL', 'id': 'CC-1002'},
    {'point': const LatLng(37.7730, -122.4200), 'priority': 'LOW', 'id': 'CC-1003'},
    {'point': const LatLng(37.7780, -122.4150), 'priority': 'MEDIUM', 'id': 'CC-1004'},
    {'point': const LatLng(37.7720, -122.4250), 'priority': 'HIGH', 'id': 'CC-1005'},
  ];

  Color _getPriorityColor(String priority) {
    switch (priority) {
      case 'CRITICAL': return Colors.black;
      case 'HIGH': return Colors.red;
      case 'MEDIUM': return Colors.orange;
      case 'LOW': return Colors.green;
      default: return Colors.blue;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('City Overview Map'),
        actions: [
          IconButton(
            icon: const Icon(Icons.filter_list),
            onPressed: () => _showFilterBottomSheet(context),
          )
        ],
      ),
      body: FlutterMap(
        mapController: _mapController,
        options: MapOptions(
          initialCenter: _cityCenter,
          initialZoom: 13.0,
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.civiconnect.admin',
          ),
          MarkerLayer(
            markers: _adminIssues.map((issue) {
              return Marker(
                point: issue['point'],
                width: 40,
                height: 40,
                child: GestureDetector(
                  onTap: () {
                    // Show complaint details or navigate
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Tapped ${issue['id']} - ${issue['priority']}')),
                    );
                  },
                  child: Container(
                    decoration: BoxDecoration(
                      color: _getPriorityColor(issue['priority']).withOpacity(0.8),
                      shape: BoxShape.circle,
                      border: Border.all(color: Colors.white, width: 2),
                    ),
                    child: const Icon(Icons.warning_amber_rounded, color: Colors.white, size: 24),
                  ),
                ),
              );
            }).toList(),
          ),
        ],
      ),
    );
  }

  void _showFilterBottomSheet(BuildContext context) {
    showModalBottomSheet(
      context: context,
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(20))),
      builder: (context) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('Map Filters', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                _buildFilterDropdown('Category', ['All', 'Road', 'Water', 'Electricity']),
                const SizedBox(height: 12),
                _buildFilterDropdown('Priority', ['All', 'Critical', 'High', 'Medium', 'Low']),
                const SizedBox(height: 12),
                _buildFilterDropdown('Department', ['All', 'Public Works', 'Sanitation']),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Apply Filters'),
                  ),
                )
              ],
            ),
          ),
        );
      },
    );
  }

  Widget _buildFilterDropdown(String label, List<String> options) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: label, border: const OutlineInputBorder()),
      value: options.first,
      items: options.map((o) => DropdownMenuItem(value: o, child: Text(o))).toList(),
      onChanged: (val) {},
    );
  }
}
