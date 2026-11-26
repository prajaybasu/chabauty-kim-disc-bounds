module

import BBPGrouping
import all BBPGrouping.GroupedDilog
import all BBPGrouping.LogarithmicZeroEstimate
import all BBPGrouping.MirimanoffFamily
import all BBPGrouping.MirimanoffLocalExpansion
import all BBPGrouping.MirimanoffSieve
import all BBPGrouping.MixedRank
import all BBPGrouping.PolylogZeroEstimate
import all BBPGrouping.ProjectiveDisc
import all BBPGrouping.SelmerDiscBound
import all BBPGrouping.TorsionDisc
import all BBPGrouping.UniformDiscBound
import all BBPGrouping.WolstenholmeSieve
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
    unless (`BBPGrouping).isPrefixOf modName do continue
    for ax in ← Lean.collectAxioms name do
      unless #[``propext, ``Classical.choice, ``Quot.sound].contains ax do
        throwError "{name} in {modName} depends on unexpected axiom {ax}"
    count := count + 1
  if count == 0 then throwError "No project declarations found"
  logInfo m!"Audited {count} project declarations."
