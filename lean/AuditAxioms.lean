module

import ChabautyKimDiscs
import all ChabautyKimDiscs.GroupedDilog
import all ChabautyKimDiscs.LogarithmicZeroEstimate
import all ChabautyKimDiscs.MirimanoffFamily
import all ChabautyKimDiscs.MirimanoffLocalExpansion
import all ChabautyKimDiscs.MirimanoffSieve
import all ChabautyKimDiscs.MixedRank
import all ChabautyKimDiscs.PolylogZeroEstimate
import all ChabautyKimDiscs.ProjectiveDisc
import all ChabautyKimDiscs.SelmerDiscBound
import all ChabautyKimDiscs.TorsionDisc
import all ChabautyKimDiscs.UniformDiscBound
import all ChabautyKimDiscs.WolstenholmeSieve
import Lean.Util.CollectAxioms
import Lean.Elab.Command

/-! Check transitive axiom dependencies for public and private project declarations. -/

open Lean Elab Command in
run_cmd do
  let env ← getEnv
  let mut count : Nat := 0
  for (name, _) in env.constants.toList do
    let some idx := env.getModuleIdxFor? name | continue
    let modName := env.header.moduleNames[idx]!
    unless (`ChabautyKimDiscs).isPrefixOf modName do continue
    for ax in ← Lean.collectAxioms name do
      unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "{name} in {modName} depends on unexpected axiom {ax}"
    count := count + 1
  if count == 0 then throwError "No project declarations found"
  logInfo m!"Audited {count} project declarations."
