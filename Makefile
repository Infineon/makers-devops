
FQBN   ?= infineon:psoc6:cy8ckit_062s2_ai
TARGET ?= test_interrupts_single

##############################################################################################################################################################
CLANGTIDY_OUTPUT=_results/clang-tidy/check-clang-tidy
CPPCHECK_OUTPUT=_results/cppcheck/check-cppcheck

##############################################################################################################################################################

TAG=latest

IFX_DOCKER_REGISTRY=dockerregistry-v2.vih.infineon.com/ifxmakers/makers-docker:$(TAG)

DOCKER_REGISTRY=ifxmakers/makers-docker:$(TAG)
GHCR_REGISTRY=ghcr.io/infineon/makers-docker:$(TAG)

REGISTRY=$(DOCKER_REGISTRY)

# Here PWD is ./extras/makers-devops 
# Therefore, we set myLocalWorkingDir to the root of the repository
DOCKER=docker run --rm -it -v $(PWD)/../..:/myLocalWorkingDir:rw $(REGISTRY)

CODECHECK=extras/makers-devops/tools/code_checks/codeChecks.py
MERGEXML=extras/makers-devops/tools/code_checks/merge_clang_tidy_cppcheck.py
PROJECTYAML=config/project.yml
USERYAML=config/user.yml

pull-container: 
	docker pull $(REGISTRY)
	find ./tools/code_checks/ -name "*.sh" -exec chmod +x {} \;
	
run-container-check-all: pull-container
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --getAllChecks
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --runAllChecks

run-container-cppcheck: pull-container
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --runCheck check-cppcheck 

run-container-clang-tidy-check: pull-container
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --runCheck check-clang-tidy 

run-container-clang-tidy-format: pull-container
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --runCheck clang-format

run-container-black-format:
	$(DOCKER) python3 $(CODECHECK) --projectYAML $(PROJECTYAML) --userYAML $(USERYAML) --runCheck black-format

run-container-generate-html-report: pull-container
	$(DOCKER) python3 $(MERGEXML) --logDir=$(CLANGTIDY_OUTPUT) --xmlPath=$(CPPCHECK_OUTPUT)/check-cppcheck-errors.xml 
	$(DOCKER) cppcheck-htmlreport --file=$(CPPCHECK_OUTPUT)/check-cppcheck-errors.xml --title=CPPCheck --report-dir=$(CPPCHECK_OUTPUT)/html-report --source-dir=. 2>&1 | tee -a $(CPPCHECK_OUTPUT)/check-cppcheck.log
	firefox _results/cppcheck/check-cppcheck/html-report/index.html

##############################################################################################################################################################

# run stuff with container from docker hub
run-build-target: 
	(cd ../.. ; cd tests/arduino-core-tests ; make compile FQBN=$(FQBN) $(TARGET))

run-container-interactive: pull-container
	$(DOCKER)
