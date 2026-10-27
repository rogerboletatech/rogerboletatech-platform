package dev.rogerboletatech.core;

import com.tngtech.archunit.core.importer.ImportOption;
import com.tngtech.archunit.junit.AnalyzeClasses;
import com.tngtech.archunit.junit.ArchTest;
import com.tngtech.archunit.lang.ArchRule;

import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

/** Guardião da hexagonal: regra de dependência que só falha quando alguém quebra a fronteira. */
@AnalyzeClasses(packages = "dev.rogerboletatech.core", importOptions = ImportOption.DoNotIncludeTests.class)
class ArquiteturaTest {

	@ArchTest
	static final ArchRule dominioNaoConheceSpring = noClasses()
			.that().resideInAPackage("..domain..")
			.should().dependOnClassesThat().resideInAPackage("org.springframework..");

	@ArchTest
	static final ArchRule dominioNaoConheceAdaptadores = noClasses()
			.that().resideInAPackage("..domain..")
			.should().dependOnClassesThat().resideInAnyPackage("..adaptador..", "..application..");

	@ArchTest
	static final ArchRule aplicacaoNaoConheceAdaptadores = noClasses()
			.that().resideInAPackage("..application..")
			.should().dependOnClassesThat().resideInAPackage("..adaptador..");
}
