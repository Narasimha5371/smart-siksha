import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:smart_shiksha_app/main.dart';

void main() {
  testWidgets('Smart Shiksha app smoke test', (WidgetTester tester) async {
    // Set a large screen size (tablet) to avoid overflow errors in tests
    tester.view.physicalSize = const Size(2000, 3000);
    tester.view.devicePixelRatio = 1.0;

    // Reset the screen size after the test
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that our app starts and shows the home screen.
    expect(find.text('Smart Shiksha'), findsOneWidget);
    expect(find.text('Welcome to AI Tutor'), findsOneWidget);

    // Verify navigation cards are present
    expect(find.text('Lessons'), findsOneWidget);
    expect(find.text('AI Chat'), findsOneWidget);
  });
}
