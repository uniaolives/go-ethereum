'use client';
import { useEffect, useRef } from 'react';
import * as THREE from 'three';

export default function Visualiser({ hash }: { hash: string }) {
  const mount = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!mount.current) return;
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(400, 400);
    mount.current.appendChild(renderer.domElement);

    const audio = new Audio(`https://gateway.pinata.cloud/ipfs/${hash}`);
    audio.crossOrigin = 'anonymous';
    const ctx = new AudioContext();
    const src = ctx.createMediaElementSource(audio);
    const analyser = ctx.createAnalyser();
    src.connect(analyser); analyser.connect(ctx.destination);
    const data = new Uint8Array(analyser.frequencyBinCount);

    const geom = new THREE.PlaneGeometry(1, 1, 128, 1);
    const mat = new THREE.MeshBasicMaterial({ color: 0xff00ff, wireframe: true });
    const mesh = new THREE.Mesh(geom, mat);
    scene.add(mesh); camera.position.z = 2;

    function animate() {
      requestAnimationFrame(animate);
      analyser.getByteFrequencyData(data);
      const verts = geom.attributes.position.array as Float32Array;
      for (let i = 0; i < verts.length; i += 3) verts[i + 1] = data[i] / 512;
      geom.attributes.position.needsUpdate = true;
      renderer.render(scene, camera);
    }
    audio.play(); animate();
    return () => { audio.pause(); renderer.dispose(); };
  }, [hash]);
  return <div ref={mount} className="rounded overflow-hidden" />;
}
