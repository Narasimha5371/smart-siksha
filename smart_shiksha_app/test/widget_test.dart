// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'package:smart_shiksha_app/main.dart';

void main() {
  testWidgets('Smart Shiksha smoke test', (WidgetTester tester) async {
    // Set a larger screen size to avoid overflow errors
    tester.view.physicalSize = const Size(1080, 2400);
    tester.view.devicePixelRatio = 1.0;
    addTearDown(tester.view.resetPhysicalSize);

    // Mock environment variables for testing
    dotenv.testLoad(fileInput: 'API_BASE_URL=http://localhost:8000');

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the app title is present (indicating Home Screen loaded)
    expect(find.text('Smart Shiksha'), findsOneWidget);
  });
}
