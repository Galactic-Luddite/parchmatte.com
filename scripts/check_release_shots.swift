#!/usr/bin/env swift
// OCR gate for release images. It catches retired visible labels after a UI
// rename and checks that key build-6 controls survived the final composition.
import AppKit
import Vision

guard CommandLine.arguments.count == 3 else {
    fputs("usage: swift check_release_shots.swift STORE_DIR SITE_SHOTS_DIR\n", stderr)
    exit(2)
}

let storeDir = CommandLine.arguments[1]
let siteDir = CommandLine.arguments[2]
let stems = [
    "01-hero", "02-menu", "03-texture", "04-page-light",
    "05-per-window", "06-schedule",
]
let required: [String: [String]] = [
    "02-menu": ["Page Light", "Strength", "Softness"],
    "03-texture": [
        "Parchmatte", "Fine Grain", "Chalkboard", "Woven", "Imprint", "Soft Leaf", "Felt",
    ],
    "04-page-light": ["Page Light", "Candlelight", "Glow"],
    "05-per-window": ["Remove Paper from TextEdit Window", "Page Light"],
    "06-schedule": ["Sunset to Sunrise", "Page Light"],
]
let retired = ["Desk Lamp", "Linen", "Press", "Vellum"]
var failures: [String] = []

func recognizedLines(_ path: String) throws -> [String] {
    guard let image = NSImage(contentsOfFile: path),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        throw NSError(domain: "release-media", code: 1, userInfo: [
            NSLocalizedDescriptionKey: "Cannot open \(path)"
        ])
    }
    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = false
    try VNImageRequestHandler(cgImage: cgImage).perform([request])
    return (request.results ?? []).compactMap { $0.topCandidates(1).first?.string }
}

for stem in stems {
    for (kind, path) in [
        ("store", "\(storeDir)/\(stem).png"),
        ("site", "\(siteDir)/\(stem)-1600.jpg"),
    ] {
        do {
            let lines = try recognizedLines(path)
            let text = lines.joined(separator: "\n")
            for phrase in required[stem] ?? [] where !text.localizedCaseInsensitiveContains(phrase) {
                failures.append("\(kind) \(stem): missing \(phrase)")
            }
            for phrase in retired where text.localizedCaseInsensitiveContains(phrase) {
                failures.append("\(kind) \(stem): retired label \(phrase)")
            }
            if lines.contains(where: { $0.trimmingCharacters(in: .whitespacesAndNewlines) == "Matte" }) {
                failures.append("\(kind) \(stem): retired label Matte")
            }
            print("checked \(kind) \(stem)")
        } catch {
            failures.append("\(kind) \(stem): \(error)")
        }
    }
}

if !failures.isEmpty {
    failures.forEach { fputs("\($0)\n", stderr) }
    exit(1)
}
print("PASS: approved build-6 labels are visible; retired labels are absent")
