import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:go_router/go_router.dart';

class CitizenMapScreen extends StatefulWidget {
  const CitizenMapScreen({super.key});

  @override
  State<CitizenMapScreen> createState() => _CitizenMapScreenState();
}

class _CitizenMapScreenState extends State<CitizenMapScreen> {
  final MapController _mapController = MapController();
  final LatLng _currentLocation = const LatLng(37.7749, -122.4194); // Mock: SF

  final List<Marker> _nearbyIssues = [
    Marker(
      point: const LatLng(37.7750, -122.4180),
      width: 40,
      height: 40,
      child: const Icon(Icons.location_on, color: Colors.orange, size: 40),
    ),
    Marker(
      point: const LatLng(37.7730, -122.4200),
      width: 40,
      height: 40,
      child: const Icon(Icons.location_on, color: Colors.green, size: 40),
    ),
    Marker(
      point: const LatLng(37.7760, -122.4210),
      width: 40,
      height: 40,
      child: const Icon(Icons.location_on, color: Colors.red, size: 40),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Nearby Issues Map'),
      ),
      body: Stack(
        children: [
          FlutterMap(
            mapController: _mapController,
            options: MapOptions(
              initialCenter: _currentLocation,
              initialZoom: 14.0,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.civiconnect.app',
              ),
              MarkerLayer(
                markers: [
                  // Current location marker
                  Marker(
                    point: _currentLocation,
                    width: 50,
                    height: 50,
                    child: const Icon(Icons.person_pin_circle, color: Colors.blue, size: 50),
                  ),
                  ..._nearbyIssues,
                ],
              ),
            ],
          ),
          Positioned(
            bottom: 24,
            left: 24,
            right: 24,
            child: ElevatedButton.icon(
              onPressed: () => context.push('/report'),
              icon: const Icon(Icons.add_location_alt),
              label: const Text('Report Issue Here'),
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                textStyle: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
            ),
          ),
          Positioned(
            top: 16,
            right: 16,
            child: FloatingActionButton(
              heroTag: 'recenter',
              mini: true,
              onPressed: () => _mapController.move(_currentLocation, 15.0),
              child: const Icon(Icons.my_location),
            ),
          )
        ],
      ),
    );
  }
}
